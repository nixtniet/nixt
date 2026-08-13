# This file is placed in the Public Domain.


"in the beginning"


import logging
import threading
import time
import _thread


from .brokers import Clients
from .clients import Client
from .command import Cmd
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
        Mods.dir("mods", Workdir.moddir())
        Mods.dir(Main.sets.path)
        Commands.add(Cmd.cmd)
        if Main.sets.all:
            Main.sets.mods = ",".join(Mods.list())
        if Main.sets.admin:
            Commands.add(Cmd.tbl)
        if Main.sets.scanner or Main.sets.all:
            Mods.scanner()
        else:
            Mods.table()
        print(Mods.dirs)

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
