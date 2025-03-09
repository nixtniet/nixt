# This file is placed in the Public Domain.


"table"


import hashlib
import importlib
import importlib.util
import os
import threading
import types


from .errors  import debug, later
from .persist import spl
from .thread  import launch


initlock = threading.RLock()
loadlock = threading.RLock()


try:
    from .lookup import MD5
except Exception:
    MD5 = {}


class Table:

    debug  = False
    ignore = ["command", "names", "llm", "rst", "web", "udp", "wsd"]
    md5    = MD5
    mods   = {}

    @staticmethod
    def add(mod) -> None:
        Table.mods[mod.__name__] = mod

    @staticmethod
    def all(pkg, mods="") -> [types.ModuleType]:
        path = pkg.__path__[0]
        pname = pkg.__name__
        res = []
        for nme in Table.modules(path):
            if nme in Table.ignore:
                continue
            if "__" in nme:
                continue
            if mods and nme not in spl(mods):
                continue
            name = pname + "." + nme
            if not name:
                continue
            mod = Table.load(name)
            if not mod:
                continue
            res.append(mod)
        return res

    @staticmethod
    def check(name):
        spec = importlib.util.find_spec(name)
        path = spec.origin
        if md5(path) == Table.md5.get(name, None):
            return True
        debug(f"{name} md5 doesn't match")
        return False

    @staticmethod
    def get(name) -> types.ModuleType:
        return Table.mods.get(name, None)

    @staticmethod
    def inits(names, pname) -> [types.ModuleType]:
        with initlock:
            mods = []
            for name in spl(names):
                mname = pname + "." + name
                if not mname:
                    continue
                mod = Table.load(mname)
                if not mod:
                    continue
                if "init" in dir(mod):
                    thr = launch(mod.init)
                mods.append((mod, thr))
            return mods

    @staticmethod
    def load(name) -> types.ModuleType:
        with loadlock:
            for ign in Table.ignore:
                if ign in name:
                    return
            pname = ".".join(name.split(".")[:-1])
            module = Table.mods.get(name)
            if not module:
                try:
                    module = importlib.import_module(name, pname)
                    Table.add(module)
                    if Table.debug:
                        Table.mods[name].DEBUG = True
                except Exception as exc:
                    later(exc)
            return module

    @staticmethod
    def modules(path) -> [str]:
        return [
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and not x.startswith("__") and
                x not in Table.ignore
               ]


def md5(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return str(hashlib.md5(txt).hexdigest())



def __dir__():
    return (
        'Table',
    )
