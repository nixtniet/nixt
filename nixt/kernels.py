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
    opts = Default()
    sets = Default()
    version = 0


def configure(local=False, network=False):
    #Config.init = Config.sets.init or Config.init
    #Config.init = Config.init or modules()
    level(Config.sets.level or "info")
    Workdir.configure(Config.name)
    Mods.configure(local, network)
    if "a" in Config.opts:
        Config.init = modules()


def boot(txt="", doinit=False, local=False):
    parse(Config, txt)
    configure(local)
    scanner(Config.init)
    if doinit:
        init(Config.init, "w" in Config.opts)


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
