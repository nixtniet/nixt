# This file is placed in the Public Domain.


"configurations"


from .objects import Data, Dict
from .utility import Utils


class Configuration(Data):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            Dict.update(self, args[0])
        if kwargs:
            Dict.update(self, kwargs)


class MainConfig(type):

    @classmethod
    def __getattr__(cls, key):
        if key not in dir(cls):
            return ""
        return cls.__getattribute__(key)

    @classmethod
    def __str__(cls):
        return str(Methods.skip(cls.__dict__))


class Main(metaclass=MainConfig):

    name = Utils.pkgname(Configuration)
    wdr = f".{name}"


def __dir__():
    return (
        'Main',
    )
