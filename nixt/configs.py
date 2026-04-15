# This file is placed in the Public Domain.


"configurations"


import os


from .objects import Data, Object
from .utility import Utils


d = os.path.dirname
e = os.path.exists
j = os.path.join


class Configuration(Data):

    pass


class MainConfig(type):

    def __getattr__(cls, key):
        if key not in dir(cls):
            return ""
        return cls.__getattribute__(key)

    def __str__(cls):
        return str(Object.skip(cls.__dict__))


class Main(metaclass=MainConfig):

    level = "info"
    name = Utils.pkgname(MainConfig)
    wdr = f".{name}"


def __dir__():
    return (
        'Configuration',
        'Main',
        'd',
        'e',
        'j'
    )
