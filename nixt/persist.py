# This file is placed in the Public Domain.


"persistence through storage"


import json
import os
import threading


from .methods import deleted, fqn, search
from .objects import Object, update
from .serials import dump, load
from .timings import fntime
from .utility import cdir
from .workdir import getpath, long, store


lock = threading.RLock()


class Cache:

    objects = {}


def add(path, obj):
    Cache.objects[path] = obj


def get(path):
    return Cache.objects.get(path, None)


def sync(path, obj):
    try:
        update(Cache.objects[path], obj)
    except KeyError:
        add(path, obj)


def attrs(kind):
    objs = list(find(kind))
    if objs:
        return list(Object.keys(objs[0][1]))
    return []


def find(kind, selector={}, removed=False, matching=False):
    fullname = long(kind)
    for pth in fns(fullname):
        obj = get(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            add(pth, obj)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


def fns(kind):
    path = store(kind)
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield os.path.join(ddd, fll)

def last(obj, selector={}):
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


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def write(obj, path=""):
    with lock:
        if path == "":
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        sync(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'add',
        'attrs',
        'find',
        'fns',
        'get',
        'last',
        'read',
        'update',
        'write'
    )
