# This file is placed in the Public Domain.


"commands"


import importlib
import importlib.util
import inspect
import os
import sys


from .clients import Fleet
from .objects import Default
from .runtime import Main, launch, spl


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
        mname = pathtoname(path)
        mod = load(path, mname)
        if not mod:
            continue
        if "init" in dir(mod):
            thr = launch(mod.init)
            modz.append((mod, thr))
    return modz


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


"modules"


def load(path, mname=None):
    if not os.path.exists(path):
        return None
    if mname is None:
        mname = pathtoname(path)
    if mname is None:
        mname = path.split(os.sep)[-1][:-3]
    spec = importlib.util.spec_from_file_location(mname, path)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    if not module:
        return None
    sys.modules[module.__name__] = module
    spec.loader.exec_module(module)
    return module


def modules(path):
    return sorted([
                   x[:-3] for x in os.listdir(path)
                   if x.endswith(".py") and not x.startswith("__") and
                   x[:-3] not in Main.ignore
                  ])


def pathtoname(path):
    brk = __name__.split(".")[0]
    splitted = path.split(os.sep)
    res = []
    for splt in splitted[::-1]:
        if splt.endswith(".py"):
           splt = splt[:-3]
        res.append(splt)
        if splt == brk:
            break
    return ".".join(res[::-1])


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
