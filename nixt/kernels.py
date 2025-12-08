# This file is placed in the Public Domain.


"in the beginning"


import time


from .command import scan
from .loggers import level
from .methods import parse
from .package import Mods, confmod, modules, mods
from .threads import launch
from .utility import Default, spl
from .workdir import Workdir, confwdr


class Config(Default):

    debug = False
    init = ""
    level = "info"
    name = ""
    opts = ""
    sets = Default()
    version = 0


class Kernel:

    def configure(local=False, network=False):
        level(Config.sets.level or "info")
        confwdr(Config.name or "nixt")
        confmod(local, network)


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def init(names, wait=False):
    thrs = []
    for name in spl(names):
        mod = Mods.get(name)
        if "init" not in dir(mod):
            continue
        thrs.append(launch(mod.init))
    if wait:
        for thr in thrs:
            thr.join()

def scanner(names):
    for mod in mods(names):
        scan(mod)


def __dir__():
    return (
        'Config',
        'boot',
        'configure',
        'forever',
        'init',
        'scanner'
    )
