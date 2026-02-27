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

    def __getattr__(cls, key):
        return cls.__dict__.get(key, "")


class Config(Default):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
           Dict.update(self, args[0])
        if kwargs:
           Dict.update(self, kwargs)


class Static(type):

    def __new__(cls, name, bases, dct):
        for attr, value in dct.items():
            if "_" not in attr and isinstance(value, types.FunctionType):
                dct[attr] = staticmethod(value)
        return super().__new__(cls, name, bases, dct)


class Statics(metaclass=Static):

    pass


def __dir__():
    return (
        'Config',
        'Default',
        'Object',
        'Statics'
    )
