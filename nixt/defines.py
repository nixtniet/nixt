# This file is placed in the Public Domain.


"definitions"


import types


class Static(type):

    def __new__(mcs, *args, **kwargs):
        for key in dir(mcs):
            value = getattr(mcs, key, None)
            if isinstance(value, types.MethodType):
                setattr(mcs, key, staticmethod(value))


class StaticMethod:

    __metaclass__ = Static



def __dir__():
    return (
        'StaticMethod',
    )
