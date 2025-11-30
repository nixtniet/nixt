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


def scanner(names,init=False):
    mods = []
    for name in names:
        mod = Mods.get(name)
        if not mod:
            continue
        scan(mod)
        if init and "init" in dir(mod):
            thr = launch(mod.init)
            mods.append((mod, thr))
    return mods


def __dir__():
    return (
        'Kernel',
        'scanner'
    )
