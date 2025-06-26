# This file is placed in the Public Domain.


"persistence"


import datetime
import json.decoder
import os
import pathlib
import _thread


from .cache  import Cache
from .object import fqn, update
from .path   import store
from .serial import dump, load


lock = _thread.allocate_lock()


class Error(Exception):

    pass


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def getpath(obj):
    return os.path.join(store(ident(obj)))


def ident(obj):
    return os.path.join(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(path) from ex


def write(obj, path=""):
    with lock:
        if path == "":
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.update(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'Error',
        'cdir',
        'getpath',
        'ident',
        'read',
        'write'
    )
