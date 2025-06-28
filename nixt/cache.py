# This file is placed in the Public Domain.


"cache"


import datetime
import os
import threading
import time


from .object import Object, items, keys, update


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
        return Cache.objs.get(path, None)

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


def __dir__():
    return (
        'Cache',
    )
