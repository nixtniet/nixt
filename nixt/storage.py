# This file is placed in the Public Domain.


"persistence through storage"


import json
import logging
import os
import pathlib
import threading


from .methods import deleted, fqn, search
from .objects import Object, keys, update
from .serials import dump, load
from .timings import fntime
from .utility import cdir, ident


cachelock = threading.RLock()
lock = threading.RLock()


class Cache:

    kinds = {}
    paths = {}
    workdir = ""


def addpath(path, obj):
    "put object into cache."
    with cachelock:
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
    with cachelock:
        nrs = 0
        res = []
        for pth in Cache.paths:
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
            res.append((pth, obj))
        return res


def fns(kind):
    "file names by kind of object."
    if Cache.workdir:
        path = os.path.join(Cache.workdir, "store", kind)
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield strip(os.path.join(ddd, fll))


def kinds():
    "show kind on objects in cache."
    if Cache.workdir:
        return os.listdir(os.path.join(Cache.workdir, "store"))
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


def persist(path):
    "enable writing to disk."
    Cache.workdir = path
    skel()
    nr = 0
    for kind in kinds():
        for fnm in fns(kind):
            obj = Object()
            read(obj, fnm)
            nr += 1
    logging.debug(f"persist in {path} ({nr})")


def read(obj, path):
    "read object from path."
    with lock:
        if not Cache.workdir:
            return Cache.getpath(path)
        pth = os.path.join(Cache.workdir, "store", path)
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
                addpath(path, obj)
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


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


def strip(path):
    return path.split('store')[-1][1:]


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
        'write'
    )
