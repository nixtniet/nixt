# This file is placed in the Public Domain.


"configuration"


from .objects import Default


class Cfg(Default):

    name = Default.__module__.split(".")[0]


def get(obj, *keys):
    val = obj
    for key in keys:
        val = getattr(val, key, None)
        if val is None:
            return ""
    return val


def __dir__():
    return (
        'Cfg',
        'get'
    )
