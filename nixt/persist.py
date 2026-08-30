# This file is placed in the Public Domain.


"persistence"


import datetime
import json
import logging
import os
import pathlib
import threading


from .encoder import JSON
from .methods import Method
from .objects import Data
from .utility import Utils


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
    def cached(cls, path, base="store"):
        pth = os.path.join(Workdir.wdr, base, path)
        if not os.path.exists(pth):
            return False
        obj = Cache.get(pth)
        if obj:
            return obj
        obj = Data()
        cls.read(obj, pth, base)
        return obj

    @classmethod
    def ident(cls, obj):
        "return ident string for object."
        return os.path.join(Method.fqn(obj), *str(datetime.datetime.now()).split())

    @classmethod
    def read(cls, obj, path, base="store"):
        "read object from path."
        with cls.lock:
            pth = os.path.join(Workdir.wdr, base, path)
            if not os.path.exists(pth):
                return False
            with open(pth, "r", encoding="utf-8") as fpt:
                try:
                    Method.update(obj, JSON.load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    logging.error("failed read at %s: %s", pth, str(ex))
                    raise
            Cache.add(pth, obj)
            return True

    @classmethod
    def write(cls, obj, path="", base="store", skip=False):
        "write object to disk."
        with cls.lock:
            if path == "":
                path = cls.ident(obj)
            pth = os.path.join(Workdir.wdr, base, path)
            Utils.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                JSON.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


class Workdir:

    wdr = ""

    @classmethod
    def home(cls, name):
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @classmethod
    def kinds(cls):
        "show kind on objects in cache."
        assert cls.wdr
        path = os.path.join(cls.wdr, "store")
        if not os.path.exists(path):
            cls.skel()
        return os.listdir(path)

    @classmethod
    def logdir(cls, path=""):
        "return directory to logs."
        assert cls.wdr
        return os.path.join(cls.wdr, "logs", path)

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
        assert cls.wdr
        return os.path.join(cls.wdr, "mods")

    @classmethod
    def pid(cls, name):
        "return path to pid file."
        assert cls.wdr
        filename = os.path.join(cls.wdr, f"{name}.pid")
        if os.path.exists(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    @classmethod
    def skel(cls):
        "create directories."
        assert cls.wdr
        if not os.path.exists(cls.wdr):
            Utils.cdir(cls.wdr)
        path = os.path.abspath(cls.wdr)
        for wpth in ["config", "logs", "mods", "store"]:
            pth = pathlib.Path(os.path.join(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)


def __dir__():
    return (
        'Disk',
        'Workdir'
    )
