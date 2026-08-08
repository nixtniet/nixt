# This file is placed in the Public Domain.


"one config to rule them all"


from .objects import Data
from .utility import Utils


class Config(type):

    def __getattr__(cls, key):
        if key in dir(cls):
            return cls.__getattribute__(cls, key)
        return ""

    def __str__(cls):
        return str(Utils.skip(cls.__dict__))


class Main(metaclass=Config):

    gets = Data()
    level = "warning"
    name = Utils.pkgname(Data)
    sets = Data()


def __dir__():
    return (
        'Config',
        'Main'
    )
