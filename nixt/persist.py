# This file is placed in the Public Domain.


"persistence through storage"


import json
import threading


from .objects import update
from .serials import dump, load
from .workdir import cdir, getpath


lock = threading.RLock()


class Cache:

    objects = {}


def addcache(path, obj):
    Cache.objects[path] = obj


def getcache(path):
    return Cache.objects.get(path, None)


def sync(path, obj):
    try:
        update(Cache.objects[path], obj)
    except KeyError:
        addcache(path, obj)


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
             try:
                update(obj, load(fpt))
             except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def write(obj, path=""):
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
        'addcache',
        'getcache',
        'read',
        'sync',
        'write'
    )
