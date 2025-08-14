# This file is placed in the Public Domain.


"imports"


import hashlib
import importlib
import importlib.util
import os
import sys
import threading


from .run   import Main
from .utils import rlog, spl


initlock = threading.RLock()
loadlock = threading.RLock()


checksum = "ec2e91056cc56049af4546de374179d7"
checksum = ""

path = os.path.dirname(__file__)
path = os.path.join(path, "modules")
pname = f"{__package__}.modules"


def check(name, hash=""):
    mname = f"{pname}.{name}"
    pth = os.path.join(path, name + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return False
    if md5sum(pth) == (hash or MD5.get(name, None)):
        return True
    if Main.md5:
        rlog("error", f"{name} failed md5sum check")
    return False


def gettbl():
    pth = os.path.join(path, "tbl.py")
    if os.path.exists(pth) and (not checksum or (md5sum(pth) == checksum)):
        return load("tbl")
    return {}


def load(name):
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


def mods(names="", empty=False):
    res = []
    if empty:
        try:
            tbl = gettbl()
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


def modules(mdir=""):
    return sorted([
            x[:-3] for x in os.listdir(mdir or path)
            if x.endswith(".py") and not x.startswith("__") and
            x[:-3] not in Main.ignore
           ])
