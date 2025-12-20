# This file is placed in the Public Domain.


"in the beginning"


import pathlib
import os
import time


from .command import scan
from .configs import Config
from .loggers import level
from .methods import parse
from .package import mod, mods
from .threads import launch
from .utility import spl
from .workdir import Workdir, skel


def boot(txt):
    Workdir.wdr = Workdir.wdr or os.path.expanduser(f"~/.{Config.name}")
    skel()
    parse(Config, txt)
    level(Config.sets.level or Config.level or "info")


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def init(names, wait=False):
    thrs = []
    for name in spl(names):
        if name in Config.ignore and name not in spl(Config.sets.init):
            continue
        module = mod(name)
        if "init" not in dir(module):
            continue
        thrs.append(launch(module.init))
    if wait:
        for thr in thrs:
            thr.join()


def pidfile(filename):
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def scanner(names):
    for module in mods(names):
        if module.__name__ in Config.ignore and module.__name__ not in spl(Config.sets.init):
            continue
        scan(module)


def wrapped(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass


def __dir__():
    return (
        'boot',
        'forever',
        'init',
        'parse',
        'pidfile',
        'scanner',
        'wrapped'
    )
