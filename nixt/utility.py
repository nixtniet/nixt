# This file is placed in the Public Domain.


"dumpyard"


import datetime
import inspect
import os
import pathlib


from .methods import fqn


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def md5sum(path):
    import hashlib
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return hashlib.md5(txt, usedforsecurity=False).hexdigest()


def spl(txt):
    try:
        result = txt.split(",")
    except (TypeError, ValueError):
        result = []
    return [x for x in result if x]


def where(obj):
    return os.path.dirname(inspect.getfile(obj))


def __dir__():
    return (
        'cdir',
        'ident',
        'md5sum',
        'spl',
        'where'
    )
