# This file is placed in the Public Domain.


"booting"


import logging
import threading
import time
import _thread


from .clients import Client
from .configs import Main
from .loggers import Logging
from .package import Commands, Mods
from .parsers import Parse
from .persist import Workdir
from .utility import Md5, Utils


class Boot:

    command = Commands.command
    parse = Parse.parse
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
    def wrapped(cls, func, *args):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Client.block.set()
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Boot',
    )
