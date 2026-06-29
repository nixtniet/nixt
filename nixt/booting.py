# This file is placed in the Public Domain.


"in the beginning"


import logging
import threading
import time
import _thread


from .clients import Output
from .configs import Main
from .loggers import Logging
from .package import Mods
from .persist import Workdir
from .threads import Task, Thread
from .utility import Md5, Utils


class Boot:

    @classmethod
    def banner(cls):
        "hello."
        tmr = time.ctime(time.time()).replace("  ", " ")
        txt = "%s %s since %s %s (%s)" % (
            Main.name.upper(),
            Main.version,
            tmr,
            Main.level.upper() or "WARNING",
            Md5.core()
        )
        return txt.replace("  ", " ")

    @classmethod
    def configure(cls):
        "configure program."
        Workdir.wdr = Main.path or Workdir.home(Main.name)
        Mods.dir(f"{Main.name}.modules", Main.moddir or Utils.moddir())
        Mods.dir("modules", Workdir.moddir())
        if Main.user:
            Mods.dir("mods", "mods")
        Logging.size(len(Main.name))
        Logging.level(Main.level or "warning")
        Mods.sums()
        Md5.check(Mods.core)

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(1.0)
            except (KeyboardInterrupt, EOFError):
                break

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

    scanner = Mods.scanner

    @classmethod
    def wait(cls, nr=1):
        "wait until nr threads left running."
        while 1:
            if len(threading.enumerate()) == nr:
                break
            time.sleep(0.01)

    @classmethod
    def wrapped(cls, func, *args):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Output.block.set()
            Task.block.set()
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Boot',
    )
