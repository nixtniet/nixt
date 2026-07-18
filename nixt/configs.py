# This file is placed in the Public Domain.


"one config to rule them all"


from .objects import Default, Method
from .utility import Utils


class Config(type):

    def __getattr__(cls, key):
        if key in dir(cls):
            return cls.__getattribute__(cls, key)
        return ""

    def __str__(cls):
        return str(Method.skip(cls.__dict__))


class Main(metaclass=Config):

    gets = Default()
    level = "warning"
    name = Utils.pkgname(Method)
    sets = Default()


def __dir__():
    return (
        'Config',
        'Main'
    )
