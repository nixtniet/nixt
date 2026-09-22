# This file is placed in the Public Domain.


"in the beginning"


import logging
import os
import threading
import time
import _thread


from .clients import Clients
from .display import Screen
from .loggers import Logging
from .package import Mods
from .persist import Workdir
from .threads import Thr, Thread
from .utility import Utils


logger = logging.getLogger(__name__)


class Boot:

    "at startup"

    running = threading.Event()
    stopped = threading.Event()

    @classmethod
    def banner(cls) -> str:
        "greetings."

    @classmethod
    def configure(cls, cfg) -> None:
        "setup basic variables"
        Workdir.wdr = cfg.wdr or Workdir.wdr or Workdir.home(cfg.name)
        if not cfg.nodisk:
            Workdir.skel()
        Logging.size(len(cfg.name))
        Logging.level(cfg.level or "info")
        cfg.path = os.path.normpath(cfg.path)
        pkgname = cfg.path.split(os.sep)[-1]
        Mods.dir(cfg.path, pkgname)

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
    def init(cls, names, wait=False) -> bool:
        "call init of modules that have an init function."
        thrs = []
        for name in Utils.spl(names):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Thread.launch(mod.init))
        if thrs and wait:
            for thr in thrs:
                try:
                    thr.join()
                except (KeyboardInterrupt, EOFError):
                    _thread.interrupt_main()
        return True

    @classmethod
    def shutdown(cls) -> None:
        "call stop on clients."
        logger.debug("shutdown")
        Clients.shutdown()
        while True:
            if len(threading.enumerate()) <= 2:
                break
            time.sleep(0.01)
        cls.stopped.set()

    @classmethod
    def wrapped(cls, func, *args) -> None:
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Screen.block.set()
            Thr.block.set()
            _thread.interrupt_main()
        except Exception as ex:
            logger.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Boot',
    )
