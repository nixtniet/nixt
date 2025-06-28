# This file is placed in the Public Domain.


"cache"


import datetime
import os
import threading
import time


from .disk   import fetch, sync
from .object import fqn, items, keys, update


lock      = threading.RLock()
writelock = threading.RLock()


class Cache:

    names = []
    objs = {}

    @staticmethod
    def add(path, obj):
        with lock:
            Cache.objs[path] = obj
            typ = path.split(os.sep)[0]
            if typ not in Cache.names:
                Cache.names.append(typ)

    @staticmethod
    def get(path):
        obj = Cache.objs.get(path, None)
        if not obj:
            obj = Object()
            fetch(obj, path)
            Cache.add(path, obj)
        return obj

    @staticmethod
    def long(name):
        split = name.split(".")[-1].lower()
        res = name
        for names in Cache.types():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @staticmethod
    def typed(matcher):
        with lock:
            for key in keys(Cache.objs):
                if matcher not in key:
                     continue
                yield key

    @staticmethod
    def types():
        return Cache.names

    @staticmethod
    def update(path, obj):
        if not obj:
            return
        if path in Cache.objs:
            update(Cache.objs[path], obj)
        else:
            Cache.add(path, obj)


def read(obj, path):
    val = Cache.get(path)
    if not val:
        fetch(obj, path)
    else:
        update(obj, val)


def write(obj, path):
    Cache.update(path, obj)
    sync(obj, path)
    return path


def __dir__():
    return (
        'Cache',
        'find',
        'fns',
        'fntime',
        'last',
        'read',
        'search',
        'write'
    )
