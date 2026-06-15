# This file is placed in the Public Domain.


"in the beginning"


import os
import time
import _thread


from .configs import Main
from .loggers import Logging
from .package import Mods
from .persist import Workdir
from .threads import Task, Thread
from .utility import Md5, Utils, j


class Boot:

    @classmethod
    def configure(cls):
        "configure program."
        Workdir.wdr = Main.path or os.path.expanduser(f"~/.{Main.name}")
        Mods.dir(f"{Main.name}.modules", j(Utils.pkgdir(Boot), 'modules'))
        Mods.dir("modules", Workdir.moddir())
        if Main.user:
            Mods.dir("mods", "mods")
            Mods.dir("other", "other")
        Logging.size(len(Main.name))
        Logging.level(Main.level)
        Task.bork = Main.bork
        if Main.md5:
            Mods.sums()

    @classmethod
    def core(cls):
        "calculate md5 of the statics module."
        try:
            from . import statics
        except (ModuleNotFoundError, ImportError, SyntaxError):
            return ""
        return Md5.source(Utils.source(statics))[:7].upper()

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(0.01)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @classmethod
    def init(cls, modlist, wait=False):
        "call init of modules that have an init function."
        thrs = []
        for name in Utils.spl(modlist):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Thread.launch(mod.init))
        if thrs and wait:
            for thr in thrs:
                try:
                    thr.join()
                except (KeyboardInterrupt, EOFError):
                    return False
        return True


def __dir__():
    return (
        'Boot',
    )
