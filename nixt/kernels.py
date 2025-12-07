# This file is placed in the Public Domain.


"in the beginning"


import time


from nixt.command import scan
from nixt.loggers import level
from nixt.methods import parse
from nixt.package import Mods,  modules, mods
from nixt.threads import launch
from nixt.utility import Default, spl
from nixt.workdir import Workdir


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
        Workdir.configure(Config.name or "nixt")
        Mods.configure(local, network)


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
