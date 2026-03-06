# This file is placed in the Public Domain.


"configurations"


from .objects import Data, Dict
from .utility import Utils


class Configuration(Data):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            Dict.update(self, args[0])
        if kwargs:
            Dict.update(self, kwargs)


class Main(Configuration):

    debug = False
    default = ""
    ignore = ""
    level = "info"
    name = Utils.pkgname(Configuration)
    version = 1
    wdr = f".{name}"


def __dir__():
    return (
        'Main',
    )
