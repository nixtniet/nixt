# This file is placed in the Public Domain.


from .objects import Default


class Config(Default):

    debug = False
    name = ""
    version = 0


def __dir__():
    return (
        'Config',
    )
