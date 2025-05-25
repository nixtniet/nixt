# This file is placed in the Public Domain.


"persistence"


import datetime
import json.decoder
import os
import pathlib
import threading
import types


from typing import Dict, Iterator


from .json   import dump, load
from .object import Object, fqn, update
from .store  import store


lock = threading.RLock()
p    = os.path.join


class Error(Exception):

    pass


class Cache:

    objs: Dict[str, Object] = {}

    @staticmethod
    def add(path: str, obj: Object):
        Cache.objs[path] = obj

    @staticmethod
    def get(path: str) -> Object|None:
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher: str) -> Iterator[Object|None]:
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def cdir(path: str) -> None:
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def getpath(obj: Object) -> str:
    return p(store(ident(obj)))


def ident(obj: Object) -> str:
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj: Object, path: str) -> None:
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(path) from ex


def write(obj: Object, path: str = "") -> str|None:
    with lock:
        if path == "":
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return path


def __dir__():
    return (
        'Cache',
        'Error',
        'cdir',
        'getpath',
        'ident',
        'read',
        'write'
    )
