# This file is placed in the Public Domain.


"in the beginning"


import os


from nixt.defines import Logging, Md5, Thread, Utils, j


from .command import Commands
from .configs import Main
from .package import Mods
from .persist import Workdir


class Boot:

    @classmethod
    def configure(cls):
        "configure program."
        Workdir.wdr = Main.path or os.path.expanduser(f"~/.{Main.name}")
        Mods.add(f"{Main.name}.modules", j(Utils.pkgdir(Boot), 'modules'))
        Mods.add("modules", Workdir.moddir())
        if Main.user:
            Mods.add("mods", "mods")
            Mods.add("other", "other")
        Logging.size(len(Main.name))
        Logging.level(Main.level)
        Commands.bork = Main.bork
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

    @classmethod
    def scanner(cls):
        for name in Mods.list():
            mod = Mods.get(name)
            Commands.scan(mod)


def __dir__():
    return (
        'Boot',
    )
