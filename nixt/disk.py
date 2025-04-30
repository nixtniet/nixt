# This file is placed in the Public Domain.


"disk"


import json
import pathlib
import threading


from .json   import dump, load
from .object import update
from .store  import path


lock = threading.RLock()


class Error(Exception):

    pass


class Cache:

    objs = {}

    @staticmethod
    def add(pth, obj) -> None:
        Cache.objs[pth] = obj

    @staticmethod
    def get(pth):
        return Cache.objs.get(pth, None)

    @staticmethod
    def typed(matcher) -> []:
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def cdir(pth) -> None:
    pth = pathlib.Path(pth)
    pth.parent.mkdir(parents=True, exist_ok=True)


def read(obj, pth) -> str:
    with lock:
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(pth) from ex
    return pth


def write(obj, pth=None) -> str:
    with lock:
        if pth is None:
            pth = path(obj)
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return pth


def __dir__():
    return (
        'Cache',
        'Error',
        'cdir',
        'read',
        'write'
    )
