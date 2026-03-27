# This file is placed in the Public Domain.


"configuration"


from .objects import Data, Methods, Object
from .utility import Utils


class Configuration(Data):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            Object.update(self, args[0])
        if kwargs:
            Object.update(self, kwargs)


class MainConfig(type):

    def __getattr__(cls, key):
        if key not in dir(cls):
            return ""
        return cls.__getattribute__(key)

    def __str__(cls):
        return str(Methods.skip(cls.__dict__))


class Main(metaclass=MainConfig):

    name = Utils.pkgname(MainConfig)
    wdr = f".{name}"


def __dir__():
    return (
        'Config',
        'MainConfig',
        'Main'
    )
