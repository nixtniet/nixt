# This file is placed in the Public Domain.


"locate"


import os
import time
import types


from typing import Any, Dict, Iterator, no_type_check


from .disk   import Cache, read
from .object import Object, fqn, items, update
from .store  import long, skel, store


def fns(clz: str) -> Iterator[str]:
    pth = store(clz)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in dirs:
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    for fll in os.listdir(ddd):
                        yield os.path.join(ddd, fll)


def fntime(daystr: str) -> float:
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


def find(clz: str, selector: dict={}, deleted: bool=False, matching: bool=False) -> list[tuple[str, Object]]:
    skel()
    res = []
    clz = long(clz)
    for pth in fns(clz):
        obj = Cache.get(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            Cache.add(pth, obj)
        if not deleted and isdeleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        res.append((pth, obj))
    return sorted(res, key=lambda x: fntime(x[0]))


@no_type_check
def isdeleted(obj: Object) -> bool:
    return '__deleted__' in dir(obj) and obj.__deleted__


def last(obj: Object, selector: Dict[str, Any] = {}) -> Object|str:
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


def search(obj: Object, selector: dict, matching: bool) -> bool:
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


def __dir__():
    return (
        'find',
        'fns',
        'fntime',
        'ident',
        'last',
        'search'
    )
