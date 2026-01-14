# This file is placed in the Public Domain.


"persistence through storage"


import json
import threading


from nixt.methods import deleted, fqn
from nixt.objects import keys, update
from nixt.serials import dump, load
from nixt.utility import cdir, ident


lock = threading.RLock()


class Cache:

    paths = {}


def addpath(path, obj):
    "put object into cache."
    Cache.paths[path] = obj


def find(kind, selector={}, removed=False, matching=False):
    "locate objects by matching atributes."
    for pth in keys(Cache.paths):
        print(kind, pth)
        if kind not in pth:
            continue
        obj = getpath(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            addpath(pth, obj)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


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
        return Cache.getpath(path)


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
        syncpath(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'addpath',
        'getpath',
        'read',
        'syncpath',
        'write'
    )
