# This file is placed in the Public Domain.


"in the beginning"


import logging
import threading
import time
import _thread


from .brokers import Clients
from .clients import Client
from .configs import Main
from .package import Commands, Mods
from .persist import Workdir
from .threads import Task, Thread
from .utility import Logging, Utils


class Boot:

    @classmethod
    def banner(cls):
        "greetings."

    @classmethod
    def configure(cls):
        "now"
        Logging.level(Main.sets.level or "warning")
        Workdir.wdr = Main.sets.wdr or Workdir.wdr or Workdir.home(Main.name)
        Workdir.skel()
        Mods.dir(Workdir.moddir())
        Mods.dir(Mods.moddir())
        Mods.dir(Main.sets.path)
        if Main.sets.admin:
            from .minimal import adm
            Commands.scan(adm)
        if Main.sets.scanner or Main.sets.all:
            Mods.scanner()
        else:
            Mods.table()

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break

    @classmethod
    def init(cls, names, wait=False):
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
                    return False
        return True

    @classmethod
    def shutdown(cls):
        "call stop on clients."
        Clients.shutdown()
        while True:
            if len(threading.enumerate()) == 1:
                break
            time.sleep(0.1)

    @classmethod
    def wrapped(cls, func, *args):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Client.block.set()
            Task.block.set()
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Boot',
    )
