# This file is placed in the Public Domain.


"persistence through storage"


import os
import threading


from nixt.methods import deleted, fqn, search
from nixt.objects import keys, update
from nixt.serials import dump, load
from nixt.timings import fntime
from nixt.utility import ident


lock = threading.RLock()


class Cache:

    kinds = {}
    paths = {}
    workdir = ""


def addpath(path, obj):
    "put object into cache."
    Cache.paths[path] = obj
    full = path.split(os.sep)[0]
    kind = full.split(".")[-1].lower()
    if kind not in Cache.kinds:
        Cache.kinds[kind] = full


def attrs(kind):
    "show attributes for kind of objects."
    pth, obj = find(kind, nritems=1)
    if obj:
        return list(keys(obj))
    return []


def find(kind, selector={}, removed=False, matching=False, nritems=None):
    "locate objects by matching atributes."
    nrs = 0
    for pth in keys(Cache.paths):
        if kind not in pth:
            continue
        obj = getpath(pth)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        if nritems and nrs >= nritems:
            break
        nrs += 1
        yield pth, obj


def kinds():
    "show kind on objects in cache."
    return Cache.kinds


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


def getpath(path):
    "get object from cache."
    return Cache.paths.get(path, None)


def read(obj, path):
    "read object from path."
    with lock:
        if not Cache.workdir:
            return Cache.getpath(path)
        path = os.path.join(Cache.workdir, path)
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def syncpath(path, obj):
    "update cached object."
    try:
        update(Cache.paths[path], obj)
    except KeyError:
        addpath(path, obj)


def write(obj, path=""):
    "write object to disk."
    with lock:
        if path == "":
            path = ident(obj)
        if Cache.workdir == "":
            syncpath(path, obj)
            return path
        path = os.path.join(Cache.workdir, path)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
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
        'read',
        'syncpath',
        'write'
    )
