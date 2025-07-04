# This file is placed in the Public Domain.


"commands"


import importlib
import inspect
import os
import sys
import time


from .fleet  import Fleet
from .object import Default
from .thread import launch
from .utils  import spl


STARTTIME = time.time()


class Main(Default):

    debug   = False
    gets    = Default()
    ignore  = ""
    init    = ""
    level   = "warn"
    modpath = "mods"
    name    = Default.__module__.split(".")[-2]
    opts    = Default()
    otxt    = ""
    sets    = Default()
    verbose = False
    version = 340


class Commands:

    cmds  = {}
    md5   = {}
    names = {}

    @staticmethod
    def add(func, mod=None):
        Commands.cmds[func.__name__] = func
        if mod:
            Commands.names[func.__name__] = mod.__name__.split(".")[-1]

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)

    @staticmethod
    def scan(mod):
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz, mod)


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if not func:
        evt.ready()
        return
    func(evt)
    Fleet.display(evt)
    evt.ready()


def inits(names):
    modz = []
    for name in sorted(spl(names)):
        path = os.path.join(Main.modpath, name + ".py")
        mod = load(path, name)
        if not mod:
            continue
        if "init" in dir(mod):
            thr = launch(mod.init)
            modz.append((mod, thr))
    return modz


def load(path, mname=None):
    mname = mname or path.split(os.sep)[-1]
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(mname, path)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    if not module:
        return None
    spec.loader.exec_module(module)
    sys.modules[mname] = module
    return module


def modules(path):
    return sorted([
                   x[:-3] for x in os.listdir(path)
                   if x.endswith(".py") and not x.startswith("__") and
                   x[:-3] not in Main.ignore
                  ])


def parse(obj, txt=""):
    if txt == "":
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
    obj.txt    = txt
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


def scan(path):
    for fnm in os.listdir(path):
        pth = os.path.join(path, fnm)
        mod = load(pth)
        if mod:
            Commands.scan(mod)


"interface"


def __dir__():
    return (
        'STARTTIME',
        'Commands',
        'command',
        'inits',
        'load',
        'modules',
        'parse',
        'scan'
    )
