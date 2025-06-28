# This file is placed in the Public Domain.


"persistence"


import json.decoder
import os
import pathlib
import _thread


from .object import Object, fqn, items, update
from .path   import long, store
from .serial import dump, load


class Error(Exception):

    pass


lock = _thread.allocate_lock()


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def fns(clz):
    pth = store(clz)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        for dname in dirs:
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield os.path.join(ddd, fll)


def fetch(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(path) from ex


def sync(obj, path):
    with lock:
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return path


def __dir__():
    return (
        'Error',
        'cdir',
        'fetch',
        'sync'
    )
