# This file is placed in the Public Domain.


"persistence through storage"


import os


from .objects import Object


e = os.path.exists
j = os.path.join


class Cache:

    paths = {}

    @classmethod
    def add(cls, path, obj):
        "put object into cache."
        cls.paths[path] = obj

    @classmethod
    def get(cls, path):
        "get object from cache."
        return cls.paths.get(path, None)

    @classmethod
    def sync(cls, path, obj):
        "update cached object."
        try:
            Object.update(cls.paths[path], obj)
        except KeyError:
            cls.add(path, obj)


def __dir__():
    return (
        'Cache',
    )
