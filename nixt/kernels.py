# This file is placed in the Public Domain.


"at the beginning"


from .command import scan
from .configs import Config
from .loggers import level
from .methods import parse
from .package import Mods, mods
from .threads import launch
from .workdir import Workdir


class Kernel:

    @staticmethod
    def configure(txt):
        parse(Config, txt)
        level(Config.sets.get("level", "info"))
        Workdir.configure(Config.name)
        Mods.configure()


def init(names, wait=False):
    thrs = []
    for mod in mods(names):
        if init and "init" not in dir(mod):
            continue
        thr = launch(mod.init)
        if wait:
            thrs.append(thr)
    for thr in thrs:
        thr.join()


def scanner(names):
    for mod in mods(names):
        scan(mod)


def __dir__():
    return (
        'Kernel',
        'inits',
        'scanner'
    )
