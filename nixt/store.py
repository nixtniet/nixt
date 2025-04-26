# This file is placed in the Public Domain.


"read/write"


import datetime
import json
import os
import pathlib
import threading


from .json   import dump, load
from .object import fqn, update


lock = threading.RLock()
p    = os.path.join


class Error(Exception):

    pass


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr  = ""


def long(name) -> str:
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir():
    return p(Workdir.wdr, "mods")


def pidname(name) -> str:
    return p(Workdir.wdr, f"{name}.pid")


def skel() -> str:
    path = pathlib.Path(store())
    path.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(moddir())
    path.mkdir(parents=True, exist_ok=True)
    return path


def setwd(path):
    Workdir.wdr = path


def store(pth="") -> str:
    return p(Workdir.wdr, "store", pth)


def strip(pth, nmr=2) -> str:
    return os.sep.join(pth.split(os.sep)[-nmr:])


def types() -> [str]:
    return os.listdir(store())


def wdr(pth):
    return p(Workdir.wdr, pth)


def ident(obj) -> str:
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def path(obj):
    return p(store(ident(obj)))


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj) -> None:
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher) -> []:
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def cdir(pth) -> None:
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


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
        'Workdir',
        'cdir',
        'ident',
        'long',
        'moddir',
        'path',
        'pidname',
        'read',
        'search',
        'setwd',
        'skel',
        'store',
        'strip',
        'update',
        'wdr',
        'write'
    )
