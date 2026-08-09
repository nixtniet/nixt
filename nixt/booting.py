# This file is placed in the Public Domain.


"at the beginning"


from .configs import Main
from .package import Cmd, Mods
from .parsers import Parse
from .persist import Workdir


class Boot:

    @classmethod
    def boot(cls, name, args):
        Main.name = name
        Parse.parse(Main, " ".join(args))
        Workdir.configure(name)
        Mods.configure(name)
        Mods.add(Cmd.cmd)


def __dir__():
    return (
        'Boot',
    )
