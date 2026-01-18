# This file is placed in the Public Domain.


"persistence through storage"


import json
import os
import pathlib
import threading


from .methods import deleted, fqn, search
from .objects import Object, keys, update
from .serials import dump, load
from .timings import fntime
from .utility import ident


lock = threading.RLock()


class Cache:

    paths = {}
    workdir = ""


def addpath(path, obj):
    "put object into cache."
    Cache.paths[path] = obj


def getpath(path):
    "get object from cache."
    return Cache.paths.get(path, None)


def syncpath(path, obj):
    "update cached object."
    try:
        update(Cache.paths[path], obj)
    except KeyError:
        addpath(path, obj)


"workdir"


def persist(path):
    "enable writing to disk."
    Cache.workdir = path
    skel()


def kinds():
    "show kind on objects in cache."
    return os.listdir(os.path.join(Cache.workdir, "store"))

def long(name):
    "expand to fqn."
    split = name.split(".")[-1].lower()
    res = name
    for names in kinds():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def skel():
    "create directories."
    if not Cache.workdir:
        return
    path = os.path.abspath(Cache.workdir)
    workpath = os.path.join(path, "store")
    pth = pathlib.Path(workpath)
    pth.mkdir(parents=True, exist_ok=True)
    modpath = os.path.join(path, "mods")
    pth = pathlib.Path(modpath)
    pth.mkdir(parents=True, exist_ok=True)


def workdir():
    "return workdir."
    return Cache.workdir


"utility"


def cdir(path):
    "create directory."
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def strip(path):
    "strip filename from path."
    return path.split('store')[-1][1:]


"find"


def attrs(kind):
    "show attributes for kind of objects."
    pth, obj = find(kind, nritems=1)
    if obj:
        return list(keys(obj))
    return []


def find(kind, selector={}, removed=False, matching=False, nritems=None):
    "locate objects by matching atributes."
    nrs = 0
    res = []
    for pth in fns(long(kind)):
        obj = getpath(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            addpath(pth, obj)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        if nritems and nrs >= nritems:
            break
        nrs += 1
        res.append((pth, obj))
    return res


def fns(kind):
    "file names by kind of object."
    path = os.path.join(Cache.workdir, "store", kind)
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield strip(os.path.join(ddd, fll))


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


"storage"


def read(obj, path):
    "read object from path."
    with lock:
        pth = os.path.join(Cache.workdir, "store", path)
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex



def write(obj, path=""):
    "write object to disk."
    with lock:
        if path == "":
            path = ident(obj)
        pth = os.path.join(Cache.workdir, "store", path)
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        syncpath(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'addpath',
        'find',
        'getpath',
        'kinds',
        'last',
        'persist',
        'read',
        'skel',
        'strip',
        'syncpath',
        'workdir',
        'write'
    )
