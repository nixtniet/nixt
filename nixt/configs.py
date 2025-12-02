# This file is placed in the Public Domain.


"forced presence"


from .utility import Default


class Config(Default):

    debug = False
    name = ""
    version = 0


def __dir__():
    return (
        'Config',
    )
