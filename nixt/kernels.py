# This file is placed in the Public Domain.


"in the beginning"


import logging
import os
import time


from .command import Commands
from .configs import Config
from .loggers import Log
from .objects import Default, Dict
from .package import Mods
from .threads import Thread
from .utility import Utils
from .workdir import Workdir


spl = Utils.spl


class Kernel:

    @staticmethod
    def boot(txt):
        Workdir.wdr = Workdir.wdr or os.path.expanduser(f"~/.{Config.name}")
        Workdir.skel()
        Kernel.parse(Config, txt)
        Log.level(Config.sets.level or Config.level or "info")
        Mods.add("modules", Workdir.moddir())
        if "0" in Config.opts:
            Config.ignore = Mods.list()

    @staticmethod
    def forever():
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break

    @staticmethod
    def init(wait=False):
        names = Mods.list(Config.ignore)
        thrs = []
        for name in spl(names):
            if name in Config.ignore and name not in spl(Config.sets.init):
                continue
            mod = Mods.get(name)
            if "init" not in dir(mod):
                continue
            thrs.append(Thread.launch(mod.init))
        if wait:
            for thr in thrs:
                thr.join()

    @staticmethod
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

    @staticmethod
    def scanner(*cmds):
        for cmd in cmds:
            Commands.add(cmd)
        names = Mods.list()
        for mod in Mods.mods(names):
            if mod.__name__ in Config.ignore and mod.__name__ not in spl(Config.sets.init):
                continue
            Commands.scan(mod)


def __dir__():
    return (
        'Kernel',
    )
