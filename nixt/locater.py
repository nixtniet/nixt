# This file is placed in the Public Domain.


"find objects"


import os
import time


from nixt.objects import Object, fqn, items, keys, update
from nixt.persist import Cache, read
from nixt.workdir import long, store


def attrs(kind):
    objs = list(find(kind))
    if objs:
        return list(keys(objs[0][1]))
    return []


def deleted(obj):
    return "__deleted__" in dir(obj) and obj.__deleted__


def find(kind, selector={}, removed=False, matching=False):
    fullname = long(kind)
    for pth in fns(fullname):
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


def fns(kind):
    path = store(kind)
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
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


def search(obj, selector={}, matching=False):
    res = False
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            res = False
            break
        elif matching and value != val:
            res = False
            break
        elif str(value).lower() not in str(val).lower():
            res = False
            break
        else:
            res = True
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
