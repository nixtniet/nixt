# This file is placed in the Public Domain.


"persistence"


import datetime
import json
import logging
import os
import pathlib
import threading


from .configs import Main
from .objects import Default, Json, Method
from .utility import Time, Utils


class Cache:

    paths = {}

    @classmethod
    def add(cls, path, obj):
        "put object into cache."
        cls.paths[path] = obj

    @classmethod
    def get(cls, path):
        "get object from cache."
        return cls.paths.get(path, None)

    @classmethod
    def sync(cls, path, obj):
        "update cached object."
        try:
            Method.update(cls.paths[path], obj)
        except KeyError:
            cls.add(path, obj)


class Disk:

    lock = threading.RLock()

    @classmethod
    def ident(cls, obj):
        "return ident string for object."
        return os.path.join(Method.fqn(obj), *str(datetime.datetime.now()).split())

    @classmethod
    def read(cls, obj, path, base="store", error=True):
        "read object from path."
        with cls.lock:
            pth = os.path.join(Workdir.wdr, base, path)
            if not os.path.exists(pth):
                return False
            with open(pth, "r", encoding="utf-8") as fpt:
                try:
                    Method.update(obj, Json.load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    logging.error("failed read at %s: %s", pth, str(ex))
                    if error:
                        raise
                    return False
            return True

    @classmethod
    def write(cls, obj, path="", base="store", skip=False):
        "write object to disk."
        with cls.lock:
            if path == "":
                path = cls.ident(obj)
            pth = os.path.join(Workdir.wdr, base, path)
            if not os.path.exists(pth):
                Workdir.skel()
            Utils.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                Json.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


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
                        key=lambda x: Time.fntime(x[0])
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
    def last(cls, obj, selector={}):
        "last saved version."
        result = sorted(
                        cls.find(Method.fqn(obj), selector),
                        key=lambda x: Time.fntime(x[0])
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


class Workdir:

    wdr = ""

    @classmethod
    def home(cls, name):
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @classmethod
    def kinds(cls):
        "show kind on objects in cache."
        if not cls.wdr:
            cls.wdr = cls.home(Main.name)
        path = os.path.join(cls.wdr, "store")
        if not os.path.exists(path):
            cls.skel()
        return os.listdir(path)

    @classmethod
    def long(cls, name):
        "expand to fqn."
        if "." in name:
            return name
        split = name.split(".")[-1].lower()
        res = name
        for names in cls.kinds():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @classmethod
    def moddir(cls):
        "return modules directory."
        return os.path.join(cls.wdr, "mods")

    @classmethod
    def pid(cls):
        "write pidfile."
        if not cls.wdr:
            cls.wdr = cls.home(Main.name)
        filename = os.path.join(cls.wdr, f"{Main.name}.pid")
        if os.path.exists(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    @classmethod
    def skel(cls):
        "create directories."
        if not cls.wdr:
            cls.wdr = cls.home(Main.name)
        if not os.path.exists(cls.wdr):
            Utils.cdir(cls.wdr)
        path = os.path.abspath(cls.wdr)
        for wpth in ["config", "mods", "store"]:
            pth = pathlib.Path(os.path.join(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)


def __dir__():
    return (
        'Cache',
        'Disk',
        'Locate',
        'Workdir'
    )
