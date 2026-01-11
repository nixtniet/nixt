# This file is placed in the Public Domain.


"configuration"


from .objects import Default
from .utility import pkgname


class Config(Default):

    name = pkgname(Default)


Cfg = Config()


def __dir__():
    return (
        'Cfg',
    )
