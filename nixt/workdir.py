# This file is placed in the Public Domain.


"where objects are stored."


import os
import pathlib


from .utility import ident


class Workdir:

    wdr = ""


def getident(obj):
    "path for object."
    return getstore(ident(obj))


def getstore(fnm: str = ""):
    "path to store."
    return os.path.join(Workdir.wdr, "store", fnm)


def kinds():
    "stored types."
    return os.listdir(getstore())


def long(name):
    "match full qualified name by substring."
    split = name.split(".")[-1].lower()
    res = name
    for names in kinds():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir():
    "modules directory."
    return os.path.join(Workdir.wdr, "mods")


def pidfile(filename):
    "write pidfile."
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def pidname(name: str):
    "name of pidfile."
    return os.path.join(Workdir.wdr, f"{name}.pid")


def skel():
    "create directories."
    path = getstore()
    pth = pathlib.Path(path)
    pth.mkdir(parents=True, exist_ok=True)
    pth = pathlib.Path(moddir())
    pth.mkdir(parents=True, exist_ok=True)


def __dir__():
    return (
        'Workdir',
        'getident',
        'getstore',
        'kinds',
        'long',
        'moddir',
        'pidfile',
        'pidname',
        'skel'
    )
