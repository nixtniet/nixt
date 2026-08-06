# This file is placed in the Public Domain.


"disk"


import datetime
import json
import logging
import os
import pathlib
import threading


from nixt.objects import Json, Method


from .workdir import Workdir


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
    def cdir(cls, path):
        "create directory."
        if os.path.exists(path):
            return
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

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
            cls.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                Json.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


def __dir__():
    return (
        'Disk',
    )
