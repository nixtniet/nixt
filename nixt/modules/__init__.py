# This file is placed in the Public Domain.


"modules"


import importlib
import importlib.util
import inspect
import os
import sys
import threading
import time
import types
import typing
import _thread


from ..error  import later
from ..fleet  import Fleet
from ..object import Default
from ..utils  import debug, md5sum, spl


initlock = threading.RLock()
loadlock = threading.RLock()


checksum = "64878c531bcee4980eae300e23323de4"
checksum = ""


path  = f"{os.path.dirname(__file__)}"
pname = f"{__package__}"


STARTTIME = time.time()


class MD5Error(Exception):

    pass


class Main(Default):

    debug   = False
    ignore  = 'llm,mbx,rst,udp,web,wsd'
    init    = ""
    md5     = True
    name    = __package__.split(".")[0]
    opts    = Default()
    verbose = False


class Commands:

    cmds  = {}
    md5   = {}
    names = {}

    @staticmethod
    def add(func, mod=None) -> None:
        Commands.cmds[func.__name__] = func
        if mod:
            Commands.names[func.__name__] = mod.__name__.split(".")[-1]

    @staticmethod
    def get(cmd) -> typing.Callable:
        if not Commands.names:
            tbl = gettbl("NAMES")
            if tbl:
                Commands.names.update(tbl)
        func = Commands.cmds.get(cmd, None)
        if not func:
            name = Commands.names.get(cmd, None)
            if not name:
                return
            if not check(name):
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
        Fleet.display(evt)
    evt.ready()


def parse(obj, txt=None) -> None:
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args   = []
    obj.cmd    = ""
    obj.gets   = Default()
    obj.index  = None
    obj.mod    = ""
    obj.opts   = ""
    obj.result = {}
    obj.sets   = Default()
    obj.silent = Default()
    obj.txt    = txt or ""
    obj.otxt   = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            setattr(obj.silent, key, value)
            setattr(obj.gets, key, value)
            continue
        elif "==" in spli:
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


def scan(mod) -> None:
    for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmdz.__code__.co_varnames:
            Commands.add(cmdz, mod)


"utilities"


def check(name, sum=""):
    if not checksum:
        return True
    if not Commands.md5:
        md5s = gettbl("MD5")
        if md5s:
            Commands.md5.update(md5s)
    mname = f"{pname}.{name}"
    pth = os.path.abspath(mname.replace(".", os.sep) + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return False
    if md5sum(pth) == (sum or MD5.get(name, None)):
        return True
    debug(f"{name} failed md5sum check")
    return False


def getmod(name):
    mname = f"{pname}.{name}"
    pth = os.path.abspath(mname.replace(".", os.sep) + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gettbl(name):
    pth = os.path.join(path, "tbl.py")
    mname = f"{pname}.tbl"
    if not checksum or (md5sum(pth) == checksum):
        mod = getmod("tbl")
        if mod:
            return getattr(mod, name, None)


def load(name) -> types.ModuleType:
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


def modules(mdir="") -> [str]:
    return [
            x[:-3] for x in os.listdir(mdir or path)
            if x.endswith(".py") and not x.startswith("__") and
            x not in Main.ignore
           ]


"interface"


def __dir__():
    return (
        'STARTTIME',
        'Commands',
        'check',
        'command',
        'getmod',
        'gettbl',
        'inits',
        'load',
        'modules',
        'mods',
        'md5',
        'parse',
        'scan'
    )
