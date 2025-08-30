# This file is placed in the Public Domain.


"modules management"


import hashlib
import importlib
import logging
import os
import sys
import threading


loadlock = threading.RLock()


class Mods:

    checksum = "fd204fbc5dbe4417ccc7f5d0ee9080f6"
    loaded   = []
    md5s     = {}
    ignore   = []
    path     = os.path.dirname(__file__)
    path     = os.path.join(path, "modules")
    pname    = f"{__package__}.modules"


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return hashlib.md5(txt).hexdigest()


def mod(name, debug=False):
    with loadlock:
        module = None
        mname = f"{Mods.pname}.{name}"
        module = sys.modules.get(mname, None)
        if not module:
            pth = os.path.join(Mods.path, f"{name}.py")
            if not os.path.exists(pth):
                return None
            if md5sum(pth) == (hash or Mods.md5s.get(name, None)):
                logging.error(f"md5 doesn't match on {pth}")
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
        if not mod:
            continue
        res.append(module)
    return res


def modules(mdir=""):
    return sorted([
            x[:-3] for x in os.listdir(mdir or Mods.path)
            if x.endswith(".py") and not x.startswith("__") and
            x[:-3] not in Mods.ignore
           ])


def spl(txt):
    try:
        result = txt.split(",")
    except (TypeError, ValueError):
        result = [
            txt,
        ]
    return [x for x in result if x]


def sums(md5):
    pth = os.path.join(Mods.path, "tbl.py")
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
        'Mods',
        'mod',
        'mods',
        'modules',
        'spl',
        'sums'
    )
