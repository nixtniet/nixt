# This file is placed in the Public Domain.


"persistence through storage"


import json
import threading


from .objects import update
from .serials import dump, load
from .utility import cdir
from .workdir import getident


lock = threading.RLock()


class Cache:

    paths = {}


def addpath(path, obj):
    "put object into cache."
    Cache.paths[path] = obj


def getpath(path):
    "get object from cache."
    return Cache.paths.get(path, None)


def read(obj, path):
    "read object from path."
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def syncpath(path, obj):
    "update cached object."
    try:
        update(Cache.paths[path], obj)
    except KeyError:
        addpath(path, obj)


def write(obj, path=""):
    "write object to disk."
    with lock:
        if path == "":
            path = getident(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        syncpath(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'addpath',
        'getpath',
        'read',
        'syncpath',
        'write'
    )
