# This file is placed in the Public Domain.


"persistence"


import json
import os
import threading
import time


from .objects import Object, dump, items, load, update
from .persist import cdir, fntime, fqn, isdeleted, long, search


j    = os.path.join
lock = threading.RLock()


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



def find(clz, selector=None, deleted=False, matching=False):
    clz = long(clz)
    if selector is None:
        selector = {}
    for pth in  Cache.objsclz):
        if clz not in pth:
            continue
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


def read(obj, path):
    with lock:
        update(obj, Cache.objs.get(path, {}))


def write(obj, path=None):
    with lock:
        if path is None:
            path = getpath(obj)
        if path in Cache.objs:
            update(Cache.objs[path],  obj)
        else:
            Cache.objs[path] = obj


"interface"


def __dir__():
    return (
        'Cache',
        'find',
        'last',
        'read',
        'write'
    )
