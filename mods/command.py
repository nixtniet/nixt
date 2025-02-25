# This file is placed in the Public Domain.


"NIXT"


import importlib
import inspect
import os
import sys
import threading
import time
import types
import typing


from nixt.errors import later
from nixt.find   import spl
from nixt.object import Default
from nixt.thread import launch


STARTTIME = time.time()


initlock = threading.RLock()
loadlock = threading.RLock()


class Config(Default):

    init    = ""
    name    = sys.argv[0].split(os.sep)[-1]
    opts    = Default()


def gettable():
    try:
        from .names import NAMES
    except Exception:
        #later(ex)
        NAMES = {}
    return NAMES


class Table:

    debug   = False
    ignore  = ["command", "names", "llm", "rst", "web", "udp", "wsd"]
    mods    = {}

    @staticmethod
    def add(mod) -> None:
        Table.mods[mod.__name__] = mod

    @staticmethod
    def all(pkg, mods="") -> [types.ModuleType]:
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
        for ign in Table.ignore:
            if ign in name:
                return
        with loadlock:
            pname = ".".join(name.split(".")[:-1])
            module = Table.mods.get(name)
            if not module:
                try:
                    Table.mods[name] = module = importlib.import_module(name, pname)
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
                x not in Table.disable
               ]


class Commands:

    cmds = {}
    names = gettable()

    @staticmethod
    def add(func, mod=None) -> None:
        Commands.cmds[func.__name__] = func
        if mod:
            Commands.names[func.__name__] = mod.__name__

    @staticmethod
    def get(cmd) -> typing.Callable:
        return Commands.cmds.get(cmd, None)

    @staticmethod
    def getname(cmd) -> None:
        return Commands.names.get(cmd)

    @staticmethod
    def scan(mod) -> None:
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz, mod)


def command(evt) -> None:
    parse(evt)
    func = Commands.get(evt.cmd)
    if not func:
        name = Commands.names.get(evt.cmd)
        if name:
            mod = Table.load(name)
            func = getattr(mod, evt.cmd)
    if func:
        func(evt)
        evt.display()
    evt.ready()


def inits(pkg, names) -> [types.ModuleType]:
    mods = []
    path = pkg.__path__[0]
    pname = pkg.__name__
    for name in modules(pkg.__path__[0]):
        if names and name not in spl(names):
            continue
        mname = pname + "." + name
        if not mname:
            continue
        mod = getattr(pkg, name, None)
        if not mod:
             continue
        if "init" in dir(mod):
           thr = launch(mod.init)
           mods.append((mod, thr))
    return mods


def modules(path) -> [str]:
    return [
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__")
           ]


def parse(obj, txt=None) -> None:
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args    = []
    obj.cmd     = ""
    obj.gets    = Default()
    obj.index   = None
    obj.mod     = ""
    obj.opts    = ""
    obj.result  = {}
    obj.sets    = Default()
    obj.txt     = txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def scan(pkg, mods=""):
    res = []
    path = pkg.__path__[0]
    pname = pkg.__name__
    for nme in modules(path):
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
        Commands.scan(mod)
        res.append(mod)
    return res


def __dir__():
    return (
        'STARTTIME',
        'Commands',
        'Table',
        'command',
        'gettable'
        'inits',
        'parse',
        'scan',
        'spl'
    )
