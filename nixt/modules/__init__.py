# This file is placed in the Public Domain.


"modules"


import hashlib
import importlib
import importlib.util
import inspect
import os
import sys
import threading


from nixt.client import Fleet
from nixt.run    import rlog, spl


lock = threading.RLock()


class Main:

    debug    = False
    gets     = {}
    ignore   = ""
    init     = ""
    level    = "warn"
    md5      = True
    name     = __package__.split(".", maxsplit=1)[0].lower()
    opts     = {}
    otxt     = ""
    path     = ""
    sets     = {}
    verbose  = False
    version  = 410


class Commands:

    cmds  = {}
    names = {}

    @staticmethod
    def add(func, module=None) -> None:
        Commands.cmds[func.__name__] = func
        if module:
            Commands.names[func.__name__] = module.__name__.split(".")[-1]

    @staticmethod
    def get(cmd):
        func = Commands.cmds.get(cmd, None)
        if not func:
            name = Commands.names.get(cmd, None)
            if not name:
                return
            module = mod(name)
            if module:
                scan(module)
                func = Commands.cmds.get(cmd)
        return func


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


def getmod(names=""):
    res = []
    for nme in sorted(modules(Main.path)):
        if names and nme not in spl(names):
            continue
        module = mod(nme)
        if not module:
            continue
        res.append(module)
    return res


def mod(name, debug=False):
    with lock:
        module = None
        pname = Main.path.split(os.sep)[-1]
        mname = f"{pname}.{name}"
        module = sys.modules.get(mname, None)
        if not module:
            pth = os.path.join(Main.path, f"{name}.py")
            if not os.path.exists(pth):
                return None
            spec = importlib.util.spec_from_file_location(mname, pth)
            module = importlib.util.module_from_spec(spec)
            sys.modules[mname] = module
            spec.loader.exec_module(module)
        return module


def modules(mdir=""):
    pth = mdir or Main.path
    if not os.path.exists(pth):
         return []
    return sorted([
            x[:-3] for x in os.listdir(mdir or Main.path)
            if x.endswith(".py") and not x.startswith("__") and
            x[:-3] not in Main.ignore
           ])


def parse(obj, txt=None):
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args   = []
    obj.cmd    = ""
    obj.gets   = {}
    obj.index  = None
    obj.mod    = ""
    obj.opts   = ""
    obj.result = {}
    obj.sets   = {}
    obj.silent = {}
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
            obj.silent[key] = value
            obj.gets[key] = value
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            obj.gets[key] = value
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            obj.sets[key] = value
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


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmdz.__code__.co_varnames:
            Commands.add(cmdz, module)


def table():
    tbl = mod("tbl")
    names = getattr(tbl, "NAMES", None)
    if names:
        Commands.names.update(names)


def __dir__():
    return modules()
