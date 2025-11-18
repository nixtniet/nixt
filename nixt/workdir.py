# This file is placed in the Public Domain.


import datetime
import os
import pathlib
import time


from .methods import name
from .objects import Object, fqn, items, keys, update


class Workdir:

    wdr = ""

    @staticmethod
    def init(name):
        Workdir.wdr = os.path.expanduser(f"~/.{name}")


def getpath(obj):
    return store(ident(obj))


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def long(name) -> str:
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir(modname=None):
    return os.path.join(Workdir.wdr, modname or "mods")


def pidname(name):
    return os.path.join(Workdir.wdr, f"{name}.pid")


def skel():
    pth = pathlib.Path(store())
    pth.mkdir(parents=True, exist_ok=True)
    pth = pathlib.Path(moddir())
    pth.mkdir(parents=True, exist_ok=True)


def store(fnm=""):
    return os.path.join(Workdir.wdr, "store", fnm)


def types():
    return os.listdir(store())


def __dir__():
    return (
        'Workdir',
        'getpath',
        'ident',
        'long',
        'moddir',
        'pidname',
        'skel',
        'store',
        'types'
    )
