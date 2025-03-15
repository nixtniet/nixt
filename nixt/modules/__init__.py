# This file is placed in the Public Domain.


"modules"


import importlib
import importlib.util
import inspect
import hashlib
import os
import threading
import types
import typing


from ..client import Main
from ..run    import later, launch
from ..utils  import debug, parse, spl


try:
    from .tbl import NAMES, MD5
except Exception:
    NAMES = MD5 = {}


path = f"{os.path.dirname(__file__)}"
pname = f"{__package__}"


initlock = threading.RLock()
loadlock = threading.RLock()


class MD5Error(Exception):

    pass


class Commands:

    cmds = {}
    names = NAMES or {} 

    @staticmethod
    def add(func, mod=None) -> None:
        Commands.cmds[func.__name__] = func
        if mod:
            Commands.names[func.__name__] = mod.__name__.split(".")[-1]

    @staticmethod
    def get(cmd) -> typing.Callable:
        func = Commands.cmds.get(cmd, None)
        if not func:
            name = Commands.names.get(cmd, None)
            if not name:
                return
            mod = load(name)
            if mod:
                scan(mod)
                func = Commands.cmds.get(cmd)
        return func


def command(evt) -> None:
    parse(evt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        evt.display()
    evt.ready()


def scan(mod) -> None:
    for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmdz.__code__.co_varnames:
            Commands.add(cmdz, mod)


"utilities"


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
            mname = f".{name}"
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
        'Commands',
        'check',
        'command',
        'inits',
        'load',
        'modules',
        'mods',
        'md5',
        'scan'
    )
