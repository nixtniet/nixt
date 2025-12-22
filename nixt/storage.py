# This file is placed in the Public Domain.


"persistence through storage"


import json
import os
import threading


from .methods import deleted, fqn, search
from .objects import Object, keys, update
from .serials import dump, load
from .timings import fntime
from .utility import cdir
from .workdir import getpath, long, storage


lock = threading.RLock()


class Cache:

    objects = {}


def cache(path):
    "return object from cache."
    return Cache.objects.get(path, None)


def put(path, obj):
    "put object into cache."
    Cache.objects[path] = obj


def read(obj, path):
    "read object from path."
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def sync(path, obj):
    "update cached object."
    try:
        update(Cache.objects[path], obj)
    except KeyError:
        put(path, obj)


def write(obj, path=""):
    "write object to disk."
    with lock:
        if path == "":
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        sync(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'cache',
        'put',
        'read',
        'sync',
        'write'
    )
