# This file is placed in the Public Domain.


"persistence"


import datetime
import json.decoder
import os
import pathlib
import threading


from .methods import fqn
from .objects import update
from .serials import dump, loaded


j = os.path.join
lock = threading.RLock()


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr  = os.path.expanduser(f"~/.{name}")


def getpath(obj):
    return store(ident(obj))


def ident(obj):
    return j(fqn(obj), *str(datetime.datetime.now()).split())


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir():
    return j(Workdir.wdr, "mods")


def pidname(name):
    return j(Workdir.wdr, f"{name}.pid")


def setwd(name, path=""):
    path = path or os.path.expanduser(f"~/.{name}")
    Workdir.wdr = path
    skel()


def skel():
    result = ""
    if not os.path.exists(store()):
        pth = pathlib.Path(store())
        pth.mkdir(parents=True, exist_ok=True)
        pth = pathlib.Path(moddir())
        pth.mkdir(parents=True, exist_ok=True)
        result =  str(pth)
    return result


def store(pth=""):
    return j(Workdir.wdr, "store", pth)


def strip(pth, nmr=2):
    return j(pth.split(os.sep)[-nmr:])


def types():
    skel()
    return os.listdir(store())


def wdr(pth):
    return j(Workdir.wdr, pth)


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


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def write(obj, path=None):
    with lock:
        if path is None:
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.update(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'Workdir',
        'cdir',
        'long',
        'pidname',
        'read',
        'setwd',
        'store',
        'strip',
        'types',
        'write'
    )
