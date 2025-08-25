# This file is placed in the Public Domain.


"package"


import hashlib
import importlib
import importlib.util
import logging
import os
import sys
import threading


from .paths import j
from .utils import spl


lock = threading.RLock()


class Mods:

    bork     = False
    loaded   = []
    md5s     = {}
    ignore   = []
    path     = os.path.dirname(__file__)
    path     = j(path, "modules")
    pname    = f"{__package__}.modules"


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
            pth = j(Mods.path, f"{name}.py")
            if not os.path.exists(pth):
                return
            if md5sum(pth) != Mods.md5s.get(name, None):
                logging.info(f"{name} md5sum doesn't match")
                if Mods.bork:
                    return
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


def sums(md5):
    pth = j(Mods.path, "tbl.py")
    if os.path.exists(pth) and (not md5 or (md5sum(pth) == md5)):
        try:
            module = mod("tbl")
        except FileNotFoundError:
            return {}
        sms =  getattr(module, "MD5", None)
        if sms:
            Mods.md5s.update(sms)
            return True
    return False


def __dir__():
    return (
        'mod',
        'mods',
        'modules',
        'table'
    )
