# This file is placed in the Public Domain.


"at the beginning"


from .configs import Main
from .package import Cmd, Mods
from .persist import Workdir
from .utility import logging


class Boot:

    @classmethod
    def boot(cls, name, level=None):
        Main.name = name
        Workdir.configure(name)
        if level is not None:
            Logging.size(len(name))
            Logging.level(level)
        Mods.configure(name)
        Mods.add(Cmd.cmd)


def __dir__():
    return (
        'Boot',
    )
