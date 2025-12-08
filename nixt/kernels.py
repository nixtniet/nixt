# This file is placed in the Public Domain.


"in the beginning"


import time


from .command import Commands
from .loggers import Logging
from .objects import Default
from .package import Mods
from .threads import Threads
from .utility import Utils
from .workdir import Workdir


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
    def configure(local=False, network=False):
        Logging.level(Config.sets.level or "info")
        Workdir.configure(Config.name or "nixt")
        Mods.configure(local, network)

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
            thrs.append(Threads.launch(mod.init))
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
