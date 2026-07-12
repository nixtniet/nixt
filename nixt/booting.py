# This file is placed in the Public Domain.


"booting"


import logging
import threading
import time
import _thread


from .clients import Output
from .configs import Main
from .loggers import Logging
from .package import Commands, Mods
from .parsers import Parse
from .persist import Workdir
from .threads import Task, Thread
from .utility import Md5, Utils


class Boot:

    command = Commands.command
    parse = Parse.parse
    pid = Workdir.pid
    scanner = Mods.scanner

    @classmethod
    def banner(cls):
        "hello."
        tmr = time.ctime(time.time()).replace("  ", " ")
        txt = "%s since %s %s (%s)" % (
            Main.name.upper(),
            tmr,
            Main.sets.level.upper() or "WARNING",
            Md5.core()
        )
        return txt.replace("  ", " ")

    @classmethod
    def configure(cls):
        "configure program."
        Workdir.wdr = Workdir.wdr or Workdir.home(Main.name)
        Workdir.skel()
        Mods.dir("modules", Workdir.moddir())
        Logging.size(len(Main.name))
        Logging.level(Main.sets.level or "warning")
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
    def init(cls):
        "call init of modules that have an init function."
        thrs = []
        for name in Utils.spl(Main.sets.mods or Main.sets.default):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Thread.launch(mod.init))
        if thrs and Main.sets.wait:
            for thr in thrs:
                try:
                    thr.join()
                except (KeyboardInterrupt, EOFError):
                    return False
        return True

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
