# This file is placed in the Public Domain.


"cache"


import datetime
import json
import os
import threading


from .object import update
from .paths  import Workdir, cdir, j, store
from .serial import dump, load


lock = threading.RLock()


class Cache:

    objs = {}
    types = []

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(typ):
        return [x for x in Cache.objs if typ in x]

    @staticmethod
    def update(path, obj):
        if not obj:
            return
        if path in Cache.objs:
            update(Cache.objs[path], obj)
        else:
            Cache.add(path, obj)


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def read(obj, path):
    with lock:
        ppath = store(path)
        with open(ppath, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex
        Cache.update(path, obj)

 
def write(obj, path=None):
    with lock:
        if path is None:
            path = ident(obj)
        ppath = store(path)
        cdir(ppath)
        with open(ppath, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.update(path, obj)


def __dir__():
    return (
        'Cache',
        'fqn',
        'ident',
        'read',
        'write'
    )
