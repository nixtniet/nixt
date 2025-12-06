# This file is placed in the Public Domain.


"in the beginning"


import time


from nixt.command import scan
from nixt.loggers import level
from nixt.methods import parse
from nixt.package import get, list, mods
from nixt.threads import launch
from nixt.utility import Default, spl


from nixt.package import configure as confmod
from nixt.workdir import configure as confwdr


class Config(Default):

    debug = False
    init = ""
    level = "info"
    name = ""
    opts = Default()
    sets = Default()
    version = 0


def configure(local=False, network=False):
    Config.init = Config.sets.init or Config.init
    Config.init = Config.init or list()
    level(Config.sets.level or "info")
    confwdr(Config.name)
    confmod(local, network)


def boot(txt="", doinit=False, local=False):
    parse(Config, txt)
    configure(local)
    scanner(list())
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
        mod = get(name)
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
