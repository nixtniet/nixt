# This file is placed in the Public Domain.


"modules"


import importlib
import importlib.util
import os
import sys
import threading
import types


from ..objects import Default
from ..runtime import launch
from ..utility import debug, md5sum, spl


MD5 = {}
NAMES = {}


initlock = threading.RLock()
loadlock = threading.RLock()


checksum = "c8d54dcab25974fe7adce842da2f2c4e"


path  = os.path.dirname(__file__)
pname = f"{__package__}"


class Main(Default):

    debug   = False
    ignore  = 'brk,dbg,llm,mbx,udp'
    init    = ""
    md5     = True
    name    = __package__.split('.', maxsplit=1)[0]
    opts    = Default()
    verbose = False


def check(name, sum=""):
    mname = f"{pname}.{name}"
    pth = os.path.join(path, name + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return False
    if md5sum(pth) == (sum or MD5.get(name, None)):
        return True
    debug(f"{name} failed md5sum check")
    return False


def getmod(name):
    mname = f"{pname}.{name}"
    mod = sys.modules.get(mname, None)
    if mod:
        return mod
    pth = os.path.join(path, name + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules[mname] = mod
    return mod


def gettbl(name):
    pth = os.path.join(path, "tbl.py")
    if not os.path.exists(pth):
        return {}
    if not checksum or (md5sum(pth) == checksum):
        try:
            mod = getmod("tbl")
        except FileNotFoundError:
            return
        return getattr(mod, name, None)


def inits(names) -> [types.ModuleType]:
    mods = []
    for name in spl(names):
        mod = load(name)
        if not mod:
            continue
        if "init" in dir(mod):
            thr = launch(mod.init)
        mods.append((mod, thr))
    return mods


def load(name) -> types.ModuleType:
    with loadlock:
        if name in Main.ignore:
            return
        module = None
        mname = f"{pname}.{name}"
        module = sys.modules.get(mname, None)
        if not module:
            pth = os.path.join(path, f"{name}.py")
            if not os.path.exists(pth):
                return None
            spec = importlib.util.spec_from_file_location(mname, pth)
            module = importlib.util.module_from_spec(spec)
            sys.modules[mname] = module
            spec.loader.exec_module(module)
        if Main.debug:
            module.DEBUG = True
        return module


def mods(names="", empty=False) -> [types.ModuleType]:
    res = []
    if empty:
        try:
            from . import tbl
            tbl.NAMES = {}
        except ImportError:
            pass
    for nme in sorted(modules(path)):
        if names and nme not in spl(names):
            continue
        mod = load(nme)
        if not mod:
            continue
        res.append(mod)
    return res


def modules(mdir="") -> [str]:
    return [
            x[:-3] for x in os.listdir(mdir or path)
            if x.endswith(".py") and not x.startswith("__") and
            x[:-3] not in Main.ignore
           ]


def table():
    if not checksum or not Main.md5:
        return True
    md5s = gettbl("MD5")
    if not md5s:
        if Main.md5:
            print("False")
            return False
        return True
    MD5.update(md5s)
    names = gettbl("NAMES")
    if not names:
        if Main.md5:
            print("False")
            return False
        return True
    NAMES.update(names)
    return NAMES


def __dir__():
    return modules()
