# This file is placed in the Public Domain.


"in the beginning"


import os
import threading
import time
import _thread


from .brokers import Broker
from .configs import Main
from .default import Event, getLogger
from .loggers import Logging
from .package import Mods
from .persist import Workdir
from .screens import Screen
from .tasking import Task, Worker
from .typings import Callable
from .utility import Utils


Log = getLogger(__name__)


class Boot:

    "at startup"

    running: Event = Event()
    stopped: Event = Event()

    @classmethod
    def configure(cls) -> None:
        "setup basic variables"
        Workdir.wdr = Main.wdr or Workdir.wdr or Workdir.home(Main.name)
        Workdir.skel()
        Logging.size(len(Main.name))
        Logging.level(Main.level or "info")
        Main.path = os.path.normpath(Main.path)
        pkgname = Main.path.rsplit(os.sep, maxsplit=1)[-1]
        Mods.dir(Main.path, pkgname)

    @classmethod
    def forever(cls) -> None:
        "run forever until ctrl-c."
        cls.running.set()
        while cls.running.is_set():
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break
        cls.stopped.set()

    @classmethod
    def init(cls, names: str, wait: bool = False) -> bool:
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
                except (KeyboardInterrupt, EOFError):
                    _thread.interrupt_main()
        return True

    @classmethod
    def shutdown(cls, wait: bool = True) -> None:
        "call stop on clients."
        Log.debug("shutdown")
        for client in Broker.objs("wait"):
            Log.debug("wait %s", client)
            try:
                client.wait()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        for client in Broker.objs("stop"):
            Log.debug("stop %s", client)
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
    def wrapped(cls, func: Callable, *args) -> None:
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Screen.block.set()
            Worker.block.set()
            _thread.interrupt_main()
        except Exception as ex:
            Log.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Boot',
    )
