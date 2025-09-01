# This file is placed in the Public Domain.


"modules"


import hashlib
import importlib
import importlib.util
import os
import sys
import threading


from ..run import rlog, spl


lock = threading.RLock()


class Main:

    debug    = False
    gets     = {}
    init     = ""
    level    = "warn"
    md5      = True
    name     = __package__.split(".", maxsplit=1)[0].lower()
    opts     = {}
    otxt     = ""
    sets     = {}
    verbose  = False
    version  = 401


class Mods:

    checksum = ""
    loaded   = []
    md5s     = {}
    ignore   = []
    path     = os.path.dirname(__file__)
    pname    = f"{__package__}"


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return hashlib.md5(txt).hexdigest()


def mod(name, debug=False):
    with lock:
        module = None
        mname = f"{Mods.pname}.{name}"
        module = sys.modules.get(mname, None)
        if not module:
            pth = os.path.join(Mods.path, f"{name}.py")
            if not os.path.exists(pth):
                return None
            if name != "tbl" and md5sum(pth) != Mods.md5s.get(name, None):
                rlog("warn", f"md5 error on {pth.split(os.sep)[-1]}")
            spec = importlib.util.spec_from_file_location(mname, pth)
            module = importlib.util.module_from_spec(spec)
            sys.modules[mname] = module
            spec.loader.exec_module(module)
            Mods.loaded.append(module.__name__.split(".")[-1])
        if debug:
            module.DEBUG = True
        return module


def mods(names=""):
    res = []
    for nme in sorted(modules(Mods.path)):
        if names and nme not in spl(names):
            continue
        module = mod(nme)
        if not module:
            continue
        res.append(module)
    return res


def modules(mdir=""):
    return sorted([
            x[:-3] for x in os.listdir(mdir or Mods.path)
            if x.endswith(".py") and not x.startswith("__") and
            x[:-3] not in Mods.ignore
           ]) 


def sums(checksum):
    pth = os.path.join(Mods.path, "tbl.py")
    if not os.path.exists(pth):
        rlog("warn", "tbl.py is missing.")
        return False        
    if checksum and md5sum(pth) != checksum:
        rlog("warn", "table checksum error.")
        return False
    try:
        module = mod("tbl")
    except FileNotFoundError:
        rlog("warn", "table is not there.")
        return {}
    sms =  getattr(module, "MD5", None)
    if sms:
        Mods.md5s.update(sms)
        return True
    return False


def __dir__():
    return modules()
