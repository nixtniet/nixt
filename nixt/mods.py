# This file is placed in the Public Domain.


"commands"


import hashlib
import importlib
import importlib.util
import os
import sys
import threading


from .utils import spl


MD5 = {}


checksum = "b83d74190b5cd93ecc30596ad28fbd2e"
loadlock = threading.RLock()


if os.path.exists("mods"):
    path = "mods"
    pname = "mods"
else:
    path = os.path.dirname(__file__)
    path = os.path.join(path, "modules")
    pname = f"{__package__}.modules"


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return str(hashlib.md5(txt).hexdigest())


def mod(name, debug=False):
    with loadlock:
        module = None
        mname = f"{pname}.{name}"
        module = sys.modules.get(mname, None)
        if not module:
            pth = os.path.join(path, f"{name}.py")
            if not os.path.exists(pth):
                return None
            if md5sum(pth) == (hash or MD5.get(name, None)):
                return
            spec = importlib.util.spec_from_file_location(mname, pth)
            module = importlib.util.module_from_spec(spec)
            sys.modules[mname] = module
            spec.loader.exec_module(module)
        if debug:
            module.DEBUG = True
        return module


def mods(names=""):
    res = []
    for nme in sorted(modules(path)):
        if names and nme not in spl(names):
            continue
        module = mod(nme)
        if not mod:
            continue
        res.append(module)
    return res


def modules(mdir=""):
    return sorted([
            x[:-3] for x in os.listdir(mdir or path)
            if x.endswith(".py") and not x.startswith("__")
           ])


def sums():
    pth = os.path.join(path, "tbl.py")
    if os.path.exists(pth) and (not checksum or (md5sum(pth) == checksum)):
        try:
            module = mod("tbl")
        except FileNotFoundError:
            return {}
        sums =  getattr(module, "MD5", None)
        if sums:
            MD5.update(sums)
            return True
    return False


def __dir__():
    return (
        'mod',
        'mods',
        'modules',
        'table'
    )
