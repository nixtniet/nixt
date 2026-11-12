# This file is placed in the Public Domain.


"one config to rule them all"


from .methods import Methods


class Config(type):

    "config meta class"

    def __getattr__(cls, key):
        if key in dir(cls):
            return cls.__getattribute__(key)
        return ""

    def __str__(cls):
        return str(Methods.skip(cls))


class Main(metaclass=Config):

    "main config"

    level = ""
    mods = ""
    name = Methods.pkgname(Config)
    otxt = ""
    path = ""


class Cfg(metaclass=Config):

    "inheritable config"


def __dir__():
    return (
        'Cfg',
        'Config',
        'Main'
    )
