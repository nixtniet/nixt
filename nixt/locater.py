# This file is placed in the Public Domain.


"find objects in store"


import os
import threading
import time


from .methods import Method
from .objects import Default
from .persist import Cache, Disk
from .workdir import Workdir


class Locate:

    lock = threading.RLock()

    @classmethod
    def attrs(cls, kind):
        "show attributes for kind of objects."
        result = []
        for pth, obj in cls.find(kind, nritems=1):
            result.extend(Method.keys(obj))
        return set(result)

    @classmethod
    def count(cls, kind):
        "count kinds of objects."
        return len(list(cls.find(kind)))

    @classmethod
    def find(cls, kind, selector={}, removed=False, matching=False, nritems=None):
        "locate objects by matching atributes."
        with cls.lock:
            nrs = 0
            for pth in cls.fns(Workdir.long(kind)):
                obj = Cache.get(pth)
                if obj is None:
                    obj = Default()
                    Disk.read(obj, pth)
                    Cache.add(pth, obj)
                if not removed and Method.deleted(obj):
                    continue
                if selector and not Method.search(obj, selector, matching):
                    continue
                if nritems and nrs >= nritems:
                    break
                nrs += 1
                yield pth, obj
            else:
                return None, None

    @classmethod
    def first(cls, obj, selector={}):
        "return first object of a kind."
        result = sorted(
                        cls.find(Method.fqn(obj), selector),
                        key=lambda x: cls.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[0]
            Method.update(obj, inp[-1])
            res = inp[0]
        return res

    @classmethod
    def fns(cls, kind):
        "file names by kind of object."
        path = os.path.join(Workdir.wdr, "store", kind)
        for rootdir, dirs, _files in os.walk(path, topdown=True):
            for dname in dirs:
                if dname.count("-") != 2:
                    continue
                ddd = os.path.join(rootdir, dname)
                for fll in os.listdir(ddd):
                    yield cls.strip(os.path.join(ddd, fll))

    @classmethod
    def fntime(cls, daystr):
        "time from path."
        datestr = " ".join(daystr.split(os.sep)[-2:])
        datestr = datestr.replace("_", " ")
        if "." in datestr:
            datestr, rest = datestr.rsplit(".", 1)
        else:
            rest = ""
        timd = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            timd += float("." + rest)
        return float(timd)

    @classmethod
    def last(cls, obj, selector={}):
        "last saved version."
        result = sorted(
                        cls.find(Method.fqn(obj), selector),
                        key=lambda x: cls.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[-1]
            Method.update(obj, inp[-1])
            res = inp[0]
        return res

    @classmethod
    def strip(cls, path):
        "strip filename from path."
        return path.split('store')[-1][1:]


def __dir__():
    return (
        'Locater',
    )
