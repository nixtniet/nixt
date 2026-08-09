# This file is placed in the Public Domain.


"at the beginning"


from .configs import Main
from .package import Cmd, Mods
from .parsers import Parse
from .persist import Workdir
from .utility import Logging


class Boot:

    @classmethod
    def boot(cls, name, txt):
        Main.name = name
        Parse.parse(Main, txt)
        Workdir.configure(name)
        Mods.configure(name)
        Mods.add(Cmd.cmd)


def __dir__():
    return (
        'Boot',
    )
