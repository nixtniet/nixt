# This file is placed in the Public Domain.


"in the beginning."


import logging
import os
import pathlib
import time


from .command import scan
from .configs import Config
from .loggers import level
from .methods import parse
from .package import configure, mod, mods, modules
from .threads import launch
from .utility import spl
from .workdir import Workdir, skel


def boot(txt):
    "set important variables like workdir and module paths."
    Workdir.wdr = Workdir.wdr or os.path.expanduser(f"~/.{Config.name}")
    skel()
    parse(Config, txt)
    configure()
    if "ignore" in Config.sets:
        Config.ignore = Config.sets.ignore
    level(Config.sets.level or Config.level or "info")


def forever():
    "run forever until ctrl-c."
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def init(names=None, wait=False):
    "run init function of modules."
    if names is None:
        names = modules()
    mods = []
    for name in spl(names):
        module = mod(name)
        if not module:
            continue
        if "init" in dir(module):
            thr = launch(module.init)
            mods.append((module, thr))
    if wait:
        for module, thr in mods:
            thr.join()
    return mods


def pidfile(filename):
    "write pidfile."
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def scanner(names=None):
    "scan named modules for commands."
    if names is None:
        names = modules()
    mods = []
    for name in spl(names):
        module = mod(name)
        if not module:
            continue
        scan(module)
    return mods


def __dir__():
    return (
        'banner',
        'boot',
        'forever',
        'init',
        'pidfile',
        'scanner'
    )
