# This file is placed in the Public Domain.


"cache"


import datetime
import os
import threading
import time


from .object import update

lock = threading.RLock()


class Cache:

    objs = {}
    types = []

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj
        typ = fqn(obj)
        if typ not in Cache.types:
            Cache.types.append(typ)


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
    if selector is None:
        selector = {}
    for pth, obj in Cache.objs.items():
        if clz not in pth.lower():
            continue
        obj = Cache.get(pth)
        if not deleted and isdeleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


def fntime(daystr):
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.replace("_", " ")
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    timed = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        timed += float("." + rest)
    return float(timed)


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def getpath(obj):
    return ident(obj)


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def isdeleted(obj):
    return "__deleted__" in dir(obj) and obj.__deleted__


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
        update(obj, Cache.get(path))


def search(obj, selector, matching=False):
    res = False
    if not selector:
        return res
    for key, value in selector.items():
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


def write(obj, path):
    with lock:
        Cache.update(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'read',
        'write'
    )
