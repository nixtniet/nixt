# This file is placed in the Public Domain.


"modules"


import importlib
import importlib.util
import hashlib
import os
import threading
import types


from ..client import Main, debug, spl
from ..run    import later, launch


try:
    from ..lookup import MD5
except Exception:
    MD5 = {}


path = f"{os.path.dirname(__file__)}"
pname = f"{__package__}"


initlock = threading.RLock()
loadlock = threading.RLock()


class MD5Error(Exception):

    pass


def mods(names="") -> [types.ModuleType]:
    res = []
    for nme in sorted(modules(path)):
        if nme in spl(Main.ignore):
            continue
        if "__" in nme:
            continue
        if names and nme not in spl(names):
            continue
        mod = load(nme)
        if not mod:
            continue
        res.append(mod)
    return res


def check(name):
    if not Main.md5:
        return True
    mname = f"{pname}.{name}"
    spec = importlib.util.find_spec(mname)
    if not spec:
        return False
    path = spec.origin
    if md5(path) == MD5.get(name, None):
        return True
    debug(f"{name} md5 doesn't match")
    return False


def load(name) -> types.ModuleType:
    with loadlock:
        if name in Main.ignore:
            return
        module = None
        try:
            mname = f"{pname}.{name}"
            module = importlib.import_module(mname, pname)
            if Main.debug:
                module.DEBUG = True
        except Exception as exc:
            later(exc)
        return module


def md5(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return str(hashlib.md5(txt).hexdigest())


def modules(path) -> [str]:
    return [
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__") and
            x not in Main.ignore
           ]


def __dir__():
    return (
        'check',
        'inits',
        'load',
        'modules',
        'mods',
        'md5'
    )
