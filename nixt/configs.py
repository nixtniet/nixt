# This file is placed in the Public Domain.


from .objects import Object


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Config(Default):

    name = "nixt"
    version = 440


def __dir__():
    return (
        'Config',
        'Default'
    )
