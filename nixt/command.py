# This file is placed in the Public Domain.


"commands"


import hashlib
import importlib
import importlib.util
import inspect
import os
import sys
import time
import _thread


from .client  import Fleet
from .object  import Default
from .thread  import later, launch
from .utility import rlog, spl


STARTTIME = time.time()


lock  = _thread.allocate_lock()


CHECKSUM = "5206bffdc9dbf7a0967565deaabc2144"
CHECKSUM = ""
MD5      = {}
NAMES    = {}


class Main(Default):

    debug   = False
    gets    = Default()
    ignore  = "dbg,"
    init    = ""
    level   = "debug"
    md5     = True
    name    = __name__.split(".", maxsplit=1)[0]
    opts    = Default()
    otxt    = ""
    path    = "mods"
    sets    = Default()
    verbose = False
    version = 10


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
        func = Commands.cmds.get(cmd, None)
        if not func:
            name = Commands.names.get(cmd, None)
            if not name:
                return None
            if Main.md5 and not check(Main.path, name):
                return None
            mod = load(Main.path, name)
            if mod:
                Commands.scan(mod)
                func = Commands.cmds.get(cmd)
        return func

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
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


def inits(names):
    modz = []
    for name in sorted(spl(names)):
        try:
            mod = load(name)
            if not mod:
                continue
            if "init" in dir(mod):
                thr = launch(mod.init)
                modz.append((mod, thr))
        except Exception as ex:
            later(ex)
            _thread.interrupt_main()
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


"imports"


def check(path, name, md5=""):
    if not CHECKSUM:
        return True
    if sys.modules.get(mname):
        return True
    mname = f"{getname(path)}.{name}"
    pth = os.path.join(path, name + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return False
    if md5sum(pth) == (md5 or MD5.get(name, "")):
        return True
    if CHECKSUM and Main.md5:
        rlog("error", f"{name} md5sum failed.")
    return False


def getname(path):
    try:
        pname = path.split(os.sep)[-2]
    except IndexError:
        pname = path
    return pname


def gettbl(path):
    pth = os.path.join(path, "tbl.py")
    if not os.path.exists(pth):
        rlog("error", "tbl.py is not there.")
        return {}
    if CHECKSUM and (md5sum(pth) != CHECKSUM):
        rlog("error", "tbl.py checksum failed.")
        return {}
    mname = f"{getname(path)}.tbl"
    mod = sys.modules.get(mname, None)
    if not mod:
        spec = importlib.util.spec_from_file_location(mname, pth)
        if not spec or not spec.loader:
            return {}
        mod = importlib.util.module_from_spec(spec)
        if mod:
            spec.loader.exec_module(mod)
            sys.modules[mname] = mod
    return mod


def load(path, name):
    with lock:
        if name in Main.ignore:
            return None
        mname = f"{getname(path)}.{name}"
        module = sys.modules.get(mname, None)
        if module:
            return module
        pth = os.path.join(path, f"{name}.py")
        if not os.path.exists(pth):
            return None
        spec = importlib.util.spec_from_file_location(mname, pth)
        if not spec or not spec.loader:
            return None
        module = importlib.util.module_from_spec(spec)
        if not module:
            return None
        spec.loader.exec_module(module)
        sys.modules[mname] = module
        if Main.debug:
            module.DEBUG = True
        return module


def md5sum(modpath):
    with open(modpath, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return str(hashlib.md5(txt).hexdigest())


def mods(path, names=""):
    res = []
    for nme in modules(path):
        if names and nme not in spl(names):
            continue
        mod = load(nme)
        if not mod:
            continue
        res.append(mod)
    return res


def modules(path):
    return sorted([
                   x[:-3] for x in os.listdir(path)
                   if x.endswith(".py") and not x.startswith("__") and
                   x[:-3] not in Main.ignore
                  ])


def settable(path):
    Commands.names.update(table(path))


def table(path):
    tbl = gettbl(path)
    MD5.update(getattr(tbl, "MD5", {}))
    NAMES.update(getattr(tbl, "NAMES", {}))
    return NAMES


"interface"


def __dir__():
    return (
        'Commands',
        'Main',
        'command',
        'inits',
        'load',
        'parse'
    )
