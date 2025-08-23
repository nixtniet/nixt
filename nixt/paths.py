# This file is placed in the Public Domain.


"cache"


import datetime
import os
import pathlib


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr = os.path.expanduser(f"~/.{name}")

    @staticmethod
    def long(name):
        split = name.split(".")[-1].lower()
        res = name
        for names in Workdir.types():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @staticmethod
    def store(pth=""):
        return os.path.join(Workdir.wdr, "store", pth)


    @staticmethod
    def types():
        cdir(Workdir.store())
        return os.listdir(Workdir.store())


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def getpath(obj):
    return ident(obj)


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def skel():
    pth = pathlib.Path(Workdir.store())
    pth.mkdir(parents=True, exist_ok=True)
    return str(pth)


def strip(pth, nmr=3):
    return os.sep.join(pth.split(os.sep)[-nmr:])


"interface"


def __dir__():
    return (
        'Workdir',
        'cdir',
        'fqn',
        'getpath',
        'ident',
        'skel',
        'strip'
    )
