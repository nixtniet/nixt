# This file is placed in the Public Domain.


"modules"


import hashlib
import importlib
import importlib.util
import inspect
import os
import sys
import threading
import types
import typing


from ..objects import Default
from ..runtime import Fleet, launch


MD5 = {}
NAMES = {}


initlock = threading.RLock()
loadlock = threading.RLock()


checksum = "c8d54dcab25974fe7adce842da2f2c4e"
checksum = ""

path  = os.path.dirname(__file__)
pname = f"{__package__}"


class Main(Default):

    debug   = False
    ignore  = 'dbg,llm,mbx,udp,wsd'
    init    = ""
    md5     = True
    name    = sys.argv[0].split(os.sep)[-1].lower()
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



" utilities"


def check(name, sum=""):
    mname = f"{pname}.{name}"
    pth = os.path.join(path, name + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return False
    if md5sum(pth) == (sum or MD5.get(name, None)):
        return True
    debug(f"{name} failed md5sum check")
    return False


def getmod(name):
    mname = f"{pname}.{name}"
    mod = sys.modules.get(mname, None)
    if mod:
        return mod
    pth = os.path.join(path, name + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules[mname] = mod
    return mod


def gettbl(name):
    pth = os.path.join(path, "tbl.py")
    if os.path.exists(pth) and (not checksum or (md5sum(pth) == checksum)):
        try:
            mod = getmod("tbl")
        except FileNotFoundError:
            return
        return getattr(mod, name, None)
    return {}

def inits(names) -> [types.ModuleType]:
    mods = []
    for name in spl(names):
        mod = load(name)
        if not mod:
            continue
        if "init" in dir(mod):
            thr = launch(mod.init)
        mods.append((mod, thr))
    return mods


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


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return str(hashlib.md5(txt).hexdigest())


def mods(names="", empty=False) -> [types.ModuleType]:
    res = []
    if empty:
        try:
            from . import tbl
            tbl.NAMES = {}
        except ImportError:
            pass
    for nme in sorted(modules(path)):
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
            x[:-3] not in Main.ignore
           ]


def table():
    md5s = gettbl("MD5")
    if md5s:
        MD5.update(md5s)
    names = gettbl("NAMES")
    if names:
        NAMES.update(names)
        Commands.names.update(NAMES)


"debug"


def debug(*args):
    for arg in args:
        sys.stderr.write(str(arg))
        sys.stderr.write("\n")
        sys.stderr.flush()


def nodebug():
    with open('/dev/null', 'a+', encoding="utf-8") as ses:
        os.dup2(ses.fileno(), sys.stderr.fileno())


"utilities"


def elapsed(seconds, short=True) -> str:
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    yeas = int(nsec/yea)
    nsec -= yeas*yea
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
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


def spl(txt) -> str:
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


"interface"


def __dir__():
    return modules()
