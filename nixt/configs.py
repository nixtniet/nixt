# This file is placed in the Public Domain.


"one config to rule them all"


from .objects import Object
from .utility import Utils


class MainConfig(type):

    def __getattr__(cls, key):
        try:
            return cls.__getattribute__(key)
        except AttributeError:
            return ""

    def __str__(cls):
        return str(Object.skip(cls.__dict__))


class Main(metaclass=MainConfig):

    level = "warning"
    name = Utils.pkgname(MainConfig)
    version = ""
    wdr = ""


def __dir__():
    return (
        'Main'
    )
