# This file is placed in the Public Domain.


"table"


import importlib
import importlib.util
import os
import sys
import threading
import types


from .disk import spl
from .run  import debug, later, launch


initlock = threading.RLock()
loadlock = threading.RLock()


debug = False
ignore = []


def all(pkg, mods="") -> [types.ModuleType]:
    path = pkg.__path__[0]
    pname = pkg.__name__
    res = []
    for nme in sorted(modules(path)):
        if nme in ignore:
            continue
        if "__" in nme:
            continue
        if mods and nme not in spl(mods):
            continue
        mod = load(nme)
        if not mod:
            continue
        res.append(mod)
    return res


def inits(names, pname) -> [types.ModuleType]:
    with initlock:
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
        for ign in ignore:
            if ign in name:
                return
        module = None
        try:
            mname = f"nixt.modules.{name}"
            module = importlib.import_module(mname, "nixt.modules")
            if debug:
                    module.DEBUG = True
        except Exception as exc:
            later(exc)
        return module


def modules(path) -> [str]:
    return [
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__") and
            x not in ignore
           ]


def __dir__():
    return (
        'all',
        'check',
        'inits',
        'load',
        'modules',
        'mods',
        'md5'
    )
