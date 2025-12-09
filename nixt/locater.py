# This file is placed in the Public Domain.


"find objects"


import os
import time


from .methods import Methods
from .objects import Object, fqn, keys, update
from .persist import Cache, Disk
from .workdir import Workdir


class Locater:

    @staticmethod
    def attrs(kind):
        objs = list(Locater.find(kind))
        if objs:
            return list(keys(objs[0][1]))
        return []

    @staticmethod
    def find(kind, selector={}, removed=False, matching=False):
        fullname = Workdir.long(kind)
        for pth in Locater.fns(fullname):
            obj = Cache.get(pth)
            if not obj:
                obj = Object()
                Disk.read(obj, pth)
                Cache.add(pth, obj)
            if not removed and Methods.deleted(obj):
                continue
            if selector and not Methods.search(obj, selector, matching):
                continue
            yield pth, obj

    @staticmethod
    def fns(kind):
        path = Workdir.store(kind)
        for rootdir, dirs, _files in os.walk(path, topdown=True):
            for dname in dirs:
                if dname.count("-") != 2:
                    continue
                ddd = os.path.join(rootdir, dname)
                for fll in os.listdir(ddd):
                    yield os.path.join(ddd, fll)

    @staticmethod
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

    @staticmethod
    def last(obj, selector={}):
        result = sorted(
                        Locater.find(fqn(obj), selector),
                        key=lambda x: Locater.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[-1]
            update(obj, inp[-1])
            res = inp[0]
        return res


def __dir__():
    return (
        'Locater',
    )
