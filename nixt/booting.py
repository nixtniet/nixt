# This file is placed in the Public Domain.


"in the beginning"


import logging
import os
import threading
import time
import _thread


from .clients import Broker, Screen
from .configs import Main
from .default import Event
from .excepts import Errors
from .package import Mods
from .persist import Workdir
from .tasking import Task, Worker
from .utility import Logging, Utils


logger = logging.getLogger(__name__)


class Boot:

    "at startup"

    running = Event()
    stopped = Event()

    @classmethod
    def configure(cls):
        "setup basic variables"
        Workdir.wdr = Main.wdr or Workdir.wdr or Workdir.home(Main.name)
        Workdir.skel()
        Logging.size(len(Main.name))
        Logging.level(Main.level or "info")
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
            except (KeyboardInterrupt, EOFError) as ex:
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
                try:
                    thr.join()
                except Exception as ex:
                    Errors.throw(ex)
        return True

    @classmethod
    def shutdown(cls, wait=True):
        "call stop on clients."
        logger.debug("shutdown")
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
        except Exception as ex:
            Errors.throw(ex)


def __dir__():
    return (
        'Boot',
    )
