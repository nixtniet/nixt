# This file is placed in the Public Domain.


"modules"


import importlib
import importlib.util
import os
import sys
import threading
import types


from ..clients import Main
from ..runtime import launch
from ..utility import debug, md5sum, spl


MD5 = {}


initlock = threading.RLock()
loadlock = threading.RLock()


checksum = "64878c531bcee4980eae300e23323de4"
checksum = ""


path  = os.path.dirname(__file__)
pname = f"{__package__}"


def check(name, sum=""):
    if not checksum:
        return True
    if not Main.md5:
        md5s = gettbl("MD5")
        if md5s:
            MD5.update(md5s)
    mname = f"{pname}.{name}"
    pth = os.path.abspath(mname.replace(".", os.sep) + ".py")
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


def mods(names="") -> [types.ModuleType]:
    res = []
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


def __dir__():
    return (
        'check',
        'getmod',
        'gettbl',
        'inits',
        'load',
        'md5sum',
        'modules',
        'mods'
    )
