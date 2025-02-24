# This file is placed in the Public Domain.


"disk persistence"


import datetime
import os
import json
import pathlib
import threading


from .cache import Cache
from .object import dumps, fqn, loads, update


p    = os.path.join
lock = threading.RLock()


class Error(Exception):

    pass


def cdir(pth) -> None:
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def ident(obj) -> str:
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, pth):
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                obj2 = loads(ofile.read())
                update(obj, obj2)
            except json.decoder.JSONDecodeError as ex:
                raise Error(pth) from ex
    return pth


def write(obj, pth):
    with lock:
        cdir(pth)
        txt = dumps(obj, indent=4)
        Cache.objs[pth] = obj
        with open(pth, 'w', encoding='utf-8') as ofile:
            ofile.write(txt)
    return pth


def __dir__():
    return (
        'Cache',
        'DecodeError',
        'cdir',
        'read',
        'write'
    )
