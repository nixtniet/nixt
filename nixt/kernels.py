# This file is placed in the Public Domain.


"in the beginning"


import os
import time


from .command import Commands
from .configs import Config
from .package import Mods
from .threads import Thread
from .utility import Utils
from .workdir import Workdir


class Kernel:

    @staticmethod
    def boot(txt):
        Workdir.wdr = Workdir.wdr or os.path.join(f"{Config.name}")
        Workdir.skel()
        Kernel.parse(txt)
        Kernel.scanner(Mods.list())
        Kernel.init(Mods.list())

    @staticmethod
    def init(names, wait=False):
        thrs = []
        for name in Utils.spl(names):
            mod = Mods.get(name)
            if "init" not in dir(mod):
                continue
            thrs.append(Thread.launch(mod.init))
        if wait:
            for thr in thrs:
                thr.join()

    @staticmethod
    def scanner(names):
        for mod in Mods.mods(names):
            Commands.scan(mod)


def __dir__():
    return (
        'Kernel',
    )
