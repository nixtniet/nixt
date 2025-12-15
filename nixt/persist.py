# This file is placed in the Public Domain.


"persistence through storage"


import json
import os
import threading
import time


from .methods import Method
from .objects import Object
from .serials import Json
from .utility import Time, Utils
from .workdir import Workdir


lock = threading.RLock()


class Cache:

    objects = {}

    @staticmethod
    def add(path, obj):
        Cache.objects[path] = obj

    @staticmethod
    def get(path):
        return Cache.objects.get(path, None)

    @staticmethod
    def sync(path, obj):
        try:
            Object.update(Cache.objects[path], obj)
        except KeyError:
            Cache.add(path, obj)


class Disk:

    @staticmethod
    def read(obj, path):
        with lock:
            with open(path, "r", encoding="utf-8") as fpt:
                try:
                    Object.update(obj, Json.load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    ex.add_note(path)
                    raise ex

    @staticmethod
    def write(obj, path=""):
        with lock:
            if path == "":
                path = Workdir.path(obj)
            Utils.cdir(path)
            with open(path, "w", encoding="utf-8") as fpt:
                Json.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


class Locate:

    @staticmethod
    def attrs(kind):
        objs = list(Locate.find(kind))
        if objs:
            return list(Object.keys(objs[0][1]))
        return []

    @staticmethod
    def find(kind, selector={}, removed=False, matching=False):
        fullname = Workdir.long(kind)
        for pth in Locate.fns(fullname):
            obj = Cache.get(pth)
            if not obj:
                obj = Object()
                Disk.read(obj, pth)
                Cache.add(pth, obj)
            if not removed and Method.deleted(obj):
                continue
            if selector and not Method.search(obj, selector, matching):
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
    def last(obj, selector={}):
        result = sorted(
                        Locate.find(Object.fqn(obj), selector),
                        key=lambda x: Time.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[-1]
            Object.update(obj, inp[-1])
            res = inp[0]
        return res


def __dir__():
    return (
        'Cache',
        'Disk',
        'Locate'
    )
