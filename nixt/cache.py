# This file is placed in the Public Domain.


"cache"


import datetime
import os
import threading
import time


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


def find(clz, selector=None, deleted=False, matching=False):
    clz = Cache.long(clz)
    if selector is None:
        selector = {}
    for pth in Cache.typed(clz):
        obj = Cache.get(pth)
        if not deleted and isdeleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


def fntime(daystr):
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    datestr = datestr.replace("_", " ")
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return float(timed)


def isdeleted(obj):
    return '__deleted__' in dir(obj) and obj.__deleted__


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


def read(obj, path):
    val = Cache.get(path)
    if val:
        update(obj, val)


def write(obj, path):
    Cache.update(path, obj)
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
