# This file is placed in the Public Domain.


"persistence through storage"


import json
import threading


from nixt.objects import update
from nixt.serials import dump, load
from nixt.workdir import cdir, getpath


lock = threading.RLock()


class Cache:

    objects = {}


def add(path, obj):
    Cache.objects[path] = obj


def get(path):
    return Cache.objects.get(path, None)


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
             try:
                update(obj, load(fpt))
             except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex

def sync(path, obj):
    try:
        update(Cache.objects[path], obj)
    except KeyError:
        add(path, obj)


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
        'read',
        'write'
    )
