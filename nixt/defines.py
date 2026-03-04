# This file is placed in the Public Domain.


"definitions"



class Static(type):

    def __new__(cls, *args, **kwargs):
        for key in dir(cls):
            value = getattr(cls, key, None)
            if type(value) is types.MethodType:
                setattr(cls, key, staticmethod(value))


class StaticMethod:

    __metaclass__ = Static



def __dir__():
    return (
        'StaticMethod',
    )
