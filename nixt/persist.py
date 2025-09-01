# This file is placed in the Public Domain.


"persistence"


import datetime
import json
import os
import pathlib
import threading
import time


from .objects import Object, dump, fqn, items, load, update


lock = threading.RLock()


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj

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


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr = ""

    @staticmethod
    def cdir(path):
        pth = pathlib.Path(path)
        pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def ident(obj):
        return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())

    @staticmethod
    def long(name):
        split = name.split(".")[-1].lower()
        res = name
        for names in Workdir.types():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @staticmethod
    def path(obj):
        return Workdir.store(Workdir.ident(obj))

    @staticmethod
    def pidname(name):
        return os.path.join(Workdir.wdr, f"{name}.pid")


    @staticmethod
    def skel():
        if os.path.exists(Workdir.store()):
            return
        pth = pathlib.Path(Workdir.store())
        pth.mkdir(parents=True, exist_ok=True)
        return str(pth)

    @staticmethod
    def store(pth=""):
        return os.path.join(Workdir.wdr, "store", pth)

    @staticmethod
    def strip(pth, nmr=2):
        return os.path.join(pth.split(os.sep)[-nmr:])

    @staticmethod
    def types():
        Workdir.skel()
        return os.listdir(Workdir.store())


class Find:

    @staticmethod
    def find(clz, selector=None, deleted=False, matching=False):
        clz = Workdir.long(clz)
        if selector is None:
            selector = {}
        for pth in Find.fns(clz):
            obj = Cache.get(pth)
            if not obj:
                obj = Object()
                read(obj, pth)
                Cache.add(pth, obj)
            if not deleted and Find.isdeleted(obj):
                continue
            if selector and not Find.search(obj, selector, matching):
                continue
            yield pth, obj

    @staticmethod
    def fns(clz):
        pth = Workdir.store(clz)
        for rootdir, dirs, _files in os.walk(pth, topdown=False):
            for dname in dirs:
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
    def isdeleted(obj):
        return "__deleted__" in dir(obj) and obj.__deleted__

    @staticmethod
    def last(obj, selector=None):
        if selector is None:
            selector = {}
        result = sorted(Find.find(fqn(obj), selector), key=lambda x: Find.fntime(x[0]))
        res = ""
        if result:
            inp = result[-1]
            update(obj, inp[-1])
            res = inp[0]
        return res


    @staticmethod
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
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def setwd(name, path=""):
    path = path or os.path.expanduser(f"~/.{name}")
    Workdir.wdr = path
    Workdir.skel()


def write(obj, path=None):
    with lock:
        if path is None:
            path = Workdir.path(obj)
        Workdir.cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.update(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'Find',
        'Workdir',
        'read',
        'setwd',
        'write'
    )
