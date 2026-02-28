# This file is placed in the Public Domain.


"persistence through storage"


import json
import os
import pathlib
import threading


from .encoder import dump, load
from .methods import deleted, fqn, ident, search
from .objects import Default, keys, update
from .utility import fntime, pkgname


lock = threading.RLock()


'config'


class Main(Default):

    debug = False
    level = "info"
    name = pkgname(Default)
    version = 1
    wdr = f".{name}"


'cache'


class Cache:

    paths = {}

    @staticmethod
    def add(path, obj):
        "put object into cache."
        Cache.paths[path] = obj

    @staticmethod
    def get(path):
        "get object from cache."
        return Cache.paths.get(path, None)

    @staticmethod
    def sync(path, obj):
        "update cached object."
        try:
            update(Cache.paths[path], obj)
        except KeyError:
            Cache.add(path, obj)


"locate"


def attrs(kind):
    "show attributes for kind of objects."
    result = []
    for pth, obj in find(kind, nritems=1):
        result.extend(keys(obj))
    return {x for x in result}


def count(kind):
    return len(list(find(kind)))


def find(kind, selector={}, removed=False, matching=False, nritems=None):
    "locate objects by matching atributes."
    nrs = 0
    for pth in fns(long(kind)):
        obj = Cache.get(pth)
        if not obj:
            obj = Default()
            read(obj, pth)
            Cache.add(pth, obj)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        if nritems and nrs >= nritems:
            break
        nrs += 1
        yield pth, obj
    else:
        return None, None


def fns(kind):
    "file names by kind of object."
    path = os.path.join(Main.wdr, "store", kind)
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield strip(os.path.join(ddd, fll))


"workdir"


def cdir(path):
    "create directory."
    pth = pathlib.Path(path)
    if not os.path.exists(pth.parent):
        pth.parent.mkdir(parents=True, exist_ok=True)


def kinds():
    "show kind on objects in cache."
    return os.listdir(os.path.join(Main.wdr, "store"))


def long(name):
    "expand to fqn."
    if "." in name:
        return name
    split = name.split(".")[-1].lower()
    res = name
    for names in kinds():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def pidfile(name):
    "write pidfile."
    filename = os.path.join(Main.wdr, f"{name}.pid")
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))

def skel():
    "create directories."
    if not Main.wdr:
        return
    path = os.path.abspath(Main.wdr)
    workpath = os.path.join(path, "store")
    pth = pathlib.Path(workpath)
    pth.mkdir(parents=True, exist_ok=True)
    modpath = os.path.join(path, "mods")
    pth = pathlib.Path(modpath)
    pth.mkdir(parents=True, exist_ok=True)
    filespath = os.path.join(path, "files")
    pth = pathlib.Path(filespath)
    pth.mkdir(parents=True, exist_ok=True)


def setwd(path):
    "enable writing to disk."
    Main.wdr = path
    skel()

def strip(path):
    "strip filename from path."
    return path.split('store')[-1][1:]


def workdir(path=""):
    "return workdir."
    return os.path.join(Main.wdr, path)


"methods"


def first(obj, selector={}):
    "return first version of an object."
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = ""
    if result:
        inp = result[0]
        update(obj, inp[-1])
        res = inp[0]
    return res


def last(obj, selector={}):
    "last saved version."
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = ""
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def read(obj, path, base="store"):
    "read object from path."
    with lock:
        pth = os.path.join(Main.wdr, base, path)
        if not os.path.exists(pth):
            return
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex

def write(obj, path="", base="store"):
    "write object to disk."
    with lock:
        if path == "":
            path = ident(obj)
        pth = os.path.join(Main.wdr, base, path)
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.sync(path, obj)
        return path


"interface"


def __dir__():
    return (
        'Main',
        'attrs',
        'cdir',
        'find',
        'first',
        'kinds',
        'last',
        'long',
        'pidfile',
        'read',
        'setwd',
        'skel',
        'strip',
        'workdir',
        'write'
    )
