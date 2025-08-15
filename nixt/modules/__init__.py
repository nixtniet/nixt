# This file is placed in the Public Domain.


"modules"



import datetime
import importlib
import importlib.util
import inspect

import json
import json.decoder
import logging
import os
import pathlib
import sys
import threading
import time
import _thread


from ..auto   import Auto
from ..fleet  import Fleet
from ..object import Object, items, update
from ..serial import dump, load
from ..thread import launch
from ..utils  import spl


lock = threading.RLock()
loadlock = threading.RLock()


path = os.path.dirname(__file__)
pname = __package__


class Main(Auto):

    debug   = False
    ignore  = 'llm,udp,web,wsd'
    init    = ""
    level   = "warn"
    md5     = False
    name    = __package__.split(".", maxsplit=1)[0].lower()
    opts    = Auto()
    verbose = False
    version = 370


def mod(name):
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
            if x.endswith(".py") and not x.startswith("__") and
            x[:-3] not in Main.ignore
           ])


"commands"


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


def table():
    pth = os.path.join(path, "tbl.py")
    if not os.path.exists(pth):
        return
    tbl = mod("tbl")
    names = getattr(tbl, "NAMES", None)
    if names:
        Commands.names.update(names)


def parse(obj, txt=None):
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args   = []
    obj.cmd    = ""
    obj.gets   = Auto()
    obj.index  = None
    obj.mod    = ""
    obj.opts   = ""
    obj.result = {}
    obj.sets   = Auto()
    obj.silent = Auto()
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


"disk"




class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        return Cache.objs.get(path, None)

    @staticmethod
    def update(path, obj):
        if not obj:
            return
        if path in Cache.objs:
            update(Cache.objs[path], obj)
        else:
            Cache.add(path, obj)


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def write(obj, path):
    with lock:
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.update(path, obj)
        return path


"find"




def find(clz, selector=None, deleted=False, matching=False):
    clz = long(clz)
    if selector is None:
        selector = {}
    for pth in fns(clz):
        obj = Cache.get(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            Cache.add(pth, obj)
        if not deleted and isdeleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


def fns(clz):
    pth = store(clz)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        for dname in dirs:
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield os.path.join(ddd, fll)


def fntime(daystr):
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.replace("_", " ")
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    timed = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        timed += float("." + rest)
    return float(timed)


def isdeleted(obj):
    return "__deleted__" in dir(obj) and obj.__deleted__


def last(obj, selector=None):
    if selector is None:
        selector = {}
    result = sorted(find(fqn(obj), selector), key=lambda x: fntime(x[0]))
    res = ""
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def search(obj, selector, matching=False):
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower() or value == "match":
            res = True
        else:
            res = False
            break
    return res


"paths"


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr = ""


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def getpath(obj):
    return store(ident(obj))


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def pidname(name):
    return os.path.join(Workdir.wdr, f"{name}.pid")


def setwd(name, path=""):
    path = path or os.path.expanduser(f"~/.{name}")
    Workdir.wdr = path
    skel()


def skel():
    pth = pathlib.Path(store())
    pth.mkdir(parents=True, exist_ok=True)
    return str(pth)


def store(pth=""):
    return os.path.join(Workdir.wdr, "store", pth)


def strip(pth, nmr=2):
    return os.path.join(pth.split(os.sep)[-nmr:])


def types():
    return os.listdir(store())


def wdr(pth):
    return os.path.join(Workdir.wdr, pth)


"interface"


def __dir__():
    return modules()
