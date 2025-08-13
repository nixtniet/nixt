# This file is placed in the Public Domain.


"modules"


import hashlib
import importlib
import importlib.util
import inspect
import logging
import os
import sys
import threading
import typing
import types
import _thread


from nixt.auto   import Auto
from nixt.fleet  import Fleet
from nixt.thread import launch
from nixt.utils  import rlog, spl


MD5 = {}
NAMES = {}


initlock = threading.RLock()
loadlock = threading.RLock()


checksum = "a89efd6272163ed0c77cc79cdc49bec6"
checksum = ""


path  = os.path.dirname(__file__)
pname = __package__


class Main(Auto):

    debug   = False
    ignore  = 'llm,udp,web,wsd'
    init    = ""
    md5     = False
    name    = __package__.split(".", maxsplit=1)[0].lower()
    opts    = Auto()
    verbose = False
    version = 363


"imports"


def check(name, hash=""):
    mname = f"{pname}.{name}"
    pth = os.path.join(path, name + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return False
    if md5sum(pth) == (hash or MD5.get(name, None)):
        return True
    if Main.md5:
        rlog("wanr",f"{name} failed md5sum check")
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
    if os.path.exists(pth) and (not checksum or (md5sum(pth) == checksum)):
        try:
            mod = getmod("tbl")
        except FileNotFoundError:
            return
        return getattr(mod, name, None)
    return {}


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


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return str(hashlib.md5(txt).hexdigest())


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
    md5s = gettbl("MD5")
    if md5s:
        MD5.update(md5s)
    names = gettbl("NAMES")
    if names:
        NAMES.update(names)
    return NAMES


"interface"


def __dir__():
    return modules()
