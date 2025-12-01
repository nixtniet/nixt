# This file is placed in the Public Domain.


from .command import scan
from .configs import Config
from .loggers import level
from .methods import parse
from .package import Mods
from .threads import launch
from .workdir import Workdir


class Kernel:

    @staticmethod
    def configure(txt):
        parse(Config, txt)
        level(Config.sets.get("level", "info"))
        Workdir.configure(Config.name)
        Mods.configure()


def init(names):
    for mod in mods(names):
        if init and "init" in dir(mod):
            yield mod, launch(mod.init)


def mods(names):
    return {Mods.get(x) for x in sorted(names)}


def scanner(names):
    for mod in mods(names):
        scan(mod)


def __dir__():
    return (
        'Kernel',
        'inits',
        'mods',
        'scanner'
    )
