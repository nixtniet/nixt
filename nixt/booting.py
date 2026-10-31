# This file is placed in the Public Domain.


"in the beginning"


import os
import threading
import time
import _thread


from .clients import Broker, Screen
from .configs import Main
from .daemons import Daemon
from .default import Event, Log
from .loggers import Logging
from .package import Mods
from .persist import Workdir
from .tasking import Task, Worker
from .utility import Utils


logger = Log(__name__)


class Boot:

    "at startup"

    running = Event()
    stopped = Event()

    @classmethod
    def configure(cls):
        "setup basic variables"
        Workdir.wdr = Main.wdr or Workdir.wdr or Workdir.home(Main.name)
        Workdir.skel()
        Main.level = Main.level or "warning"
        Logging.size(len(Main.name))
        Logging.level(Main.level)
        if Main.path:
            Main.path = os.path.normpath(Main.path)
            pkgname = Main.path.rsplit(os.sep, maxsplit=1)[-1]
            Mods.dir(pkgname, Main.path)

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        cls.running.set()
        while cls.running.is_set():
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break
        cls.stopped.set()

    @classmethod
    def init(cls, names, wait=False):
        "call init of modules that have an init function."
        thrs = []
        for name in Utils.spl(names):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Task.start(mod.init))
        if thrs and wait:
            for thr in thrs:
                thr.join()
        return True

    @classmethod
    def shutdown(cls, wait=True):
        "call stop on clients."
        logger.info("shutdown")
        for client in Broker.objs("wait"):
            logger.debug("wait %s", client)
            try:
                client.wait()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        for client in Broker.objs("stop"):
            logger.debug("stop %s", client)
            try:
                client.stop()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        if wait:
            while True:
                if len(threading.enumerate()) <= 1:
                    break
                time.sleep(0.01)
        cls.stopped.set()

    @classmethod
    def wrapped(cls, func, *args):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Screen.block.set()
            Worker.block.set()
            _thread.interrupt_main()

    @classmethod
    def wrap(cls, func, *args, dofinal=None):
        "restore console."
        import termios
        import sys
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            old = None
        try:
            cls.wrapped(func, *args)
        except (KeyboardInterrupt, EOFError):
            pass
        if old and old[0]:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
        if dofinal:
            dofinal()


class Booting(Boot, Daemon):

    "at start"

    @classmethod
    def boot(cls):
        "starting"


def __dir__():
    return (
        'Boot',
        'Booting'
    )
