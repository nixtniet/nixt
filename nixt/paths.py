# This file is placed in the Public Domain.


"paths"


import datetime
import os
import pathlib


j = os.path.join


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr = os.path.expanduser(f"~/.{name}")


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def skel():
    pth = pathlib.Path(store())
    pth.mkdir(parents=True, exist_ok=True)
    return str(pth)


def store(pth=""):
    return j(Workdir.wdr, "store", pth)


def types():
    cdir(store())
    return os.listdir(store())


def __dir__():
    return (
        'Workdir',
        'cdir',
        'long',
        'skel',
        'store',
        'types'
    )
