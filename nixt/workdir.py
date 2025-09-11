# This file is placed in the Public Domain.


"working directory"


import datetime
import os
import pathlib


from .methods import fqn
from .utility import j


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr = os.path.expanduser(f"~/.{name}")


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
    if os.path.exists(store()):
        return
    pth = pathlib.Path(store())
    pth.mkdir(parents=True, exist_ok=True)
    pth = pathlib.Path(moddir())
    pth.mkdir(parents=True, exist_ok=True)
    return str(pth)


def store(pth=""):
    return j(Workdir.wdr, "store", pth)


def strip(pth, nmr=2):
    return j(pth.split(os.sep)[-nmr:])


def types():
    skel()
    return os.listdir(store())


def wdr(pth):
    return j(Workdir.wdr, pth)


def __dir__():
    return (
        'Workdir',
        'long',
        'pidname',
        'setwd',
        'store',
        'strip',
        'types'
    )
