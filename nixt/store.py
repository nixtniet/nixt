# This file is placed in the Public Domain.


"read/write"


import datetime
import os
import pathlib
import threading


from .object import fqn


lock = threading.RLock()
p    = os.path.join


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr  = ""


def ident(obj) -> str:
    return p(fqn(obj),*str(datetime.datetime.now()).split())


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


def path(obj):
    return p(store(ident(obj)))


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


def __dir__():
    return (
        'Workdir',
        'ident',
        'long',
        'moddir',
        'path',
        'pidname',
        'setwd',
        'skel',
        'store',
        'strip',
        'wdr'
    )
