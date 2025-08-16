# This file is placed in the Public Domain.


"commands"


import importlib
import importlib.util
import inspect
import os
import sys
import threading
import time


from .fleet import Fleet


STARTTIME = time.time()


loadlock = threading.RLock()
path = os.path.dirname(__file__)
path = os.path.join(path, "modules")
pname = f"{__package__}.modules"


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


def inits(names):
    modz = []
    for name in spl(names):
        try:
            module = mod(name)
            if not module:
                continue
            if "init" in dir(module):
                thr = launch(module.init)
                modz.append((module, thr))
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()
    return modz


def scan(mod):
    for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmdz.__code__.co_varnames:
            Commands.add(cmdz, mod)


"imports"


def mod(name, debug=False):
    with loadlock:
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
        if debug:
            module.DEBUG = True
        return module


def mods(names="", empty=False):
    res = []
    if empty:
        Commands.names = {}
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


def table():
    pth = os.path.join(path, "tbl.py")
    if not os.path.exists(pth):
        return
    tbl = mod("tbl")
    names = getattr(tbl, "NAMES", None)
    if names:
        Commands.names.update(names)


"parser"


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
        elif "==" in spli:
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


"utilities"


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365 * 24 * 60 * 60
    week = 7 * 24 * 60 * 60
    nday = 24 * 60 * 60
    hour = 60 * 60
    minute = 60
    yeas = int(nsec / yea)
    nsec -= yeas * yea
    weeks = int(nsec / week)
    nsec -= weeks * week
    nrdays = int(nsec / nday)
    nsec -= nrdays * nday
    hours = int(nsec / hour)
    nsec -= hours * hour
    minutes = int(nsec / minute)
    nsec -= int(minute * minutes)
    sec = int(nsec)
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def spl(txt):
    try:
        result = txt.split(",")
    except (TypeError, ValueError):
        result = [
            txt,
        ]
    return [x for x in result if x]


"interface"


def __dir__():
    return (
        'Commands',
        'command',
        'inits',
        'mod',
        'mods',
        'modules',
        'parse',
        'scan',
        'spl',
        'tbl'
    )
