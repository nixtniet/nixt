# This file is placed in the Public Domain.


"modules"


import sys


def getmain(name):
    main = sys.modules.get("__main__")
    return getattr(main, name)


from . import lst, thr
from . import irc, rss
from . import req, slg
from . import srv # noqa: F401
from . import fnd, log, tdo
from . import mbx, mdl, rst, web
from . import wsd as wsd
from . import udp as udp
from . import upt


__all__ = (
    'fnd',
    'irc',
    'log',
    'lst',
    'mbx',
    'mdl',
    'req',
    'rss',
    'rst',
    'slg',
    'tdo',
    'thr',
    'web',
    'udp',
    'upt',
#    'wsd'
)


def __dir__():
    return __all__
