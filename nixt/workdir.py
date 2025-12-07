# This file is placed in the Public Domain.


"where objects are stored"


import datetime
import os
import pathlib


from nixt.objects import fqn


class Workdir:

    wdr = ""

    @staticmethod
    def configure(name):
       Workdir.wdr = Workdir.wdr or os.path.expanduser(f"~/.{name}")
       skel()


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def getpath(obj):
    return store(ident(obj))


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def long(name: str):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
           res = names
           break
    return res


def moddir(modname: str = ""):
    return os.path.join(Workdir.wdr, modname or "mods")


def pidfile(filename):
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def pidname(name: str):
    return os.path.join(Workdir.wdr, f"{name}.pid")


def skel():
    path = store()
    if os.path.exists(path):
        return
    pth = pathlib.Path(path)
    pth.mkdir(parents=True, exist_ok=True)
    pth = pathlib.Path(moddir())
    pth.mkdir(parents=True, exist_ok=True)


def store(fnm: str = ""):
    return os.path.join(Workdir.wdr, "store", fnm)


def types():
    return os.listdir(store())


def __dir__():
    return (
        'Workdir',
        'cdir',
        'getpath',
        'ident',
        'lomg',
        'moddir',
        'pidfile',
        'pidname',
        'skel',
        'store',
        'types'
    )
