# This file is placed in the Public Domain.


"configurations"


from .objects import Default, Dict
from .utility import Utils


class Configuration(Default):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            Dict.update(self, args[0])
        if kwargs:
            Dict.update(self, kwargs)


class Main(Configuration):

    debug = False
    default = "irc,mdl,rss,wsd"
    ignore = "man,rst,udp,web"
    level = "info"
    name = Utils.pkgname(Configuration)
    version = 1
    wdr = f".{name}"


def __dir__():
    return (
        'Main',
    )
