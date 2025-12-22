# This file is placed in the Public Domain.


"persistence through storage"


import os


from .methods import deleted, fqn, search
from .objects import Object, keys, update
from .storage import cache, put, read
from .timings import fntime
from .workdir import long, storage


def attrs(kind):
    "show attributes for kind of objects."
    objs = list(find(kind))
    if objs:
        return list(keys(objs[0][1]))
    return []


def find(kind, selector={}, removed=False, matching=False):
    "locate objects by matching atributes."
    fullname = long(kind)
    for pth in fns(fullname):
        obj = cache(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            put(pth, obj)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


def fns(kind):
    "return file names by kind of object."
    path = storage(kind)
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield os.path.join(ddd, fll)


def last(obj, selector={}):
    "return last saved version."
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


def __dir__():
    return (
        'attrs',
        'find',
        'fns',
        'last'
    )
