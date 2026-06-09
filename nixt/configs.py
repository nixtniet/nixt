# This file is placed in the Public Domain.


"one config to rule them all"


import os


from .command import Commands
from .loggers import Logging
from .objects import Object
from .persist import Workdir
from .package import Mods
from .utility import Utils


class MainConfig(type):

    def __getattr__(cls, key):
        if key in dir(cls):
            return cls.__getattribute__(cls, key)
        return ""

    def __str__(cls):
        return str(Object.skip(cls.__dict__))


class Main(metaclass=MainConfig):

    level = "info"
    name = Utils.pkgname(Object)

 
def configure():
    "configure program."
    Workdir.wdr = Main.path or os.path.expanduser(f"~/.{Main.name}")
    Mods.add("modules", Workdir.moddir())
    if Main.user:
        Mods.add("mods", "mods")
    Logging.size(len(Main.name))
    Logging.level(Main.level)
    Mods.sums()
    Commands.table()
    Commands.bork = True


def __dir__():
    return (
        'Main',
        'configure'
    )
