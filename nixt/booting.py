# This file is placed in the Public Domain.


"in the beginning"


import os
import time
import _thread


from .loggers import Log
from .message import Message
from .package import Mods
from .persist import Workdir
from .threads import Thread
from .utility import Utils


class Boot:

    md5s = {}

    @classmethod
    def boot(cls, cfg):
        Workdir.wdr = cfg.wdr or os.path.expanduser(f"~/.{cfg.name}")
        if cfg.user:
            Mods.add("mods", "mods")
            Mods.add("other", "other")
        cls.table()
        Mods.table()
        Log.size(len(cfg.name))
        Log.level(cfg.level or "info")

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

    @classmethod
    def table(cls):
        "read table,"
        try:
            from .statics import CORE
            cls.md5s.update(CORE)
            return True
        except ImportError:
            return False


def __dir__():
    return (
        'Boot',
    )
