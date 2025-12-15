# This file is placed in the Public Domain.


"in the beginning"


import time


from .command import Commands
from .objects import Default
from .package import Mods
from .threads import Thread
from .utility import Utils


class Config(Default):

    debug = False
    init = ""
    level = "info"
    name = ""
    opts = ""
    sets = Default()
    version = 0


class Kernel:

    @staticmethod
    def forever():
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break

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
        'Config',
        'Kernel'
    )
