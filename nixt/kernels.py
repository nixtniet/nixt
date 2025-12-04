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
    level = "info"
    name = ""
    version = 0


class Kernel:

    @staticmethod
    def banner(stream):
        tme = time.ctime(time.time()).replace("  ", " ")
        stream.write("%s %s since %s (%s)" % (
                                       Config.name.upper(),
                                       Config.version,
                                       tme,
                                       Config.level.upper()
                                      ))
        stream.write("\n")
        stream.flush()

    @staticmethod
    def boot(txt, stream=None, init=True):
        Kernel.configure(txt)
        if stream and "v" in Config.opts:
            Kernel.banner(stream)
        Kernel.scanner(Mods.list())
        if init:
            Kernel.init(Config.sets.init or Mods.list(), "w" in Config.opts)

    @staticmethod
    def configure(txt):
        Methods.parse(Config, txt)
        Logging.level(Config.sets.level or "info")
        Workdir.configure(Config.name)
        Mods.configure("m" in Config.opts)

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
