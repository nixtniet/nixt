# This file is placed in the Public Domain.


import os
import time


from .methods import name
from .objects import Object, fqn, items, update
from .persist import Cache, read
from .workdir import long, store


def attrs(type):
    objs = list(find(type))
    if objs:
        return keys(objs[0][1])
    return []


def deleted(obj):
    return "__deleted__" in dir(obj) and obj.__deleted__


def find(type=None, selector=None, removed=False, matching=False):
    if selector is None:
        selector = {}
    fqn = long(type)
    for pth in fns(fqn):
        obj = Cache.get(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            Cache.add(pth, obj)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


def fns(type=None):
    if type is not None:
        type = type.lower()
    path = store()
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
            if type and type not in ddd.lower():
                continue
            for fll in os.listdir(ddd):
                yield os.path.join(ddd, fll)


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


def last(obj, selector=None):
    if selector is None:
        selector = {}
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


def search(obj, selector, matching=False):
    res = False
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower():
            res = True
        else:
            res = False
            break
    return res


def __dir__():
    return (
        'attrs',
        'deleted',
        'find',
        'fns',
        'fntime',
        'last',
        'search'
    )
