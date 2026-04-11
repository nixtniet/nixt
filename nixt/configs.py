# This file is placed in the Public Domain.


"configurations"


from .objects import Methods
from .utility import Utils


class MainConfig(type):

    def __getattr__(cls, key):
        if key not in dir(cls):
            return ""
        return cls.__getattribute__(key)

    def __str__(cls):
        return str(Methods.skip(cls.__dict__))


class Main(metaclass=MainConfig):

    level = "info"
    name = Utils.pkgname(MainConfig)
    wdr = f".{name}"


def __dir__():
    return (
        'Commands',
        'Main',
        'Mods'
    )
