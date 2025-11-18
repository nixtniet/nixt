# This file is placed in the Public Domain.


import pathlib
import threading


from .objects import Object, update
from .serials import dump, load


lock = threading.RLock()


class Cache:

    objs = Object()

    @staticmethod
    def add(path, obj):
        setattr(Cache.objs, path, obj)

    @staticmethod
    def get(path):
        return getattr(Cache.objs, path, None)

    @staticmethod
    def update(path, obj):
        setattr(Cache.objs, path, obj)


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def write(obj, path=None):
    with lock:
        if path is None:
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.update(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'read',
        'write'
    )
