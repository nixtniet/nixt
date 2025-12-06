# This file is placed in the Public Domain.


"in the beginning"


import time


from nixt.command import Commands
from nixt.loggers import Logging
from nixt.methods import Methods
from nixt.package import Mods
from nixt.threads import Threads
from nixt.utility import Default, Utils
from nixt.workdir import Workdir


class Config(Default):

    debug = False
    init = ""
    level = "info"
    name = ""
    opts = Default()
    sets = Default()
    version = 0


class Kernel:

    @staticmethod
    def boot(txt="", init=False, local=False):
        Methods.parse(Config, txt)
        Kernel.configure(local)
        Config.init = Config.sets.init or Config.init
        Config.init = Config.init or Mods.list()
        Kernel.scanner(Config.init)
        if init:
            Kernel.init(Config.init, "w" in Config.opts)

    @staticmethod
    def configure(local=False, network=False):
        Logging.level(Config.sets.level or "info")
        Workdir.configure(Config.name)
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
