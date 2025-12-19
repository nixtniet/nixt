# This file is placed in the Public Domain.


"in the beginning"


import os
import time


from .command import add, scan
from .configs import Config
from .loggers import level
from .objects import Default
from .package import dirs, list, mod, mods
from .threads import launch
from .utility import spl
from .workdir import Workdir, moddir, skel


def boot(txt):
    Workdir.wdr = Workdir.wdr or os.path.expanduser(f"~/.{Config.name}")
    skel()
    parse(Config, txt)
    level(Config.sets.level or Config.level or "info")
    dirs("modules", moddir())
    dirs('examples', 'examples')
    if "0" in Config.opts:
        Config.ignore = list()


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def init(wait=False):
    names = list(Config.ignore)
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


def parse(obj, text):
    data = {
        "args": [],
        "cmd": "",
        "gets": Default(),
        "index": None,
        "init": "",
        "opts": "",
        "otxt": text,
        "rest": "",
        "silent": Default(),
        "sets": Default(),
        "text": text
    }
    for k, v in data.items():
        setattr(obj, k, getattr(obj, k, v) or v)
    args = []
    nr = -1
    for spli in text.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            setattr(obj.silent, key, value)
            setattr(obj.gets, key. value)
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            setattr(obj.sets, key, value)
            continue
        nr += 1
        if nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.text  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.text  = obj.cmd + " " + obj.rest
    else:
        obj.text = obj.cmd or ""


def scanner(*cmds):
    for cmd in cmds:
        add(cmd)
    names = list()
    for module in mods(names):
        if module.__name__ in Config.ignore and module.__name__ not in spl(Config.sets.init):
            continue
        scan(module)


def __dir__():
    return (
        'boot',
        'forever',
        'init',
        'parse',
        'scanner'
    )
