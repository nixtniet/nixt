# This file is placed in the Public Domain.


"a clean namespace"


import types


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Config(Default):

    pass


class Static(type):

    def __new__(cls, name, bases, dct):
        for attr, value in dct.items():
            if "_" not in attr and isinstance(value, types.FunctionType):
                dct[attr] = staticmethod(value)
        return super().__new__(cls, name, bases, dct)


class Statics:

    __metaclass__ = Static


def __dir__():
    return (
        'Config',
        'Default',
        'Object',
        'Statics'
    )
