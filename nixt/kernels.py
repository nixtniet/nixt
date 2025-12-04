# This file is placed in the Public Domain.


"in the beginning"


import logging
import os
import time


from nixt.brokers import Broker
from nixt.clients import Client, CLI, Output
from nixt.command import Commands
from nixt.configs import Config
from nixt.loggers import Logging
from nixt.message import Message
from nixt.methods import Methods
from nixt.package import Mods
from nixt.persist import Disk, Locater
from nixt.repeats import Repeater
from nixt.threads import Threads
from nixt.utility import Utils
from nixt.workdir import Workdir


class Kernel:

    @staticmethod
    def banner(stream):
        tme = time.ctime(time.time()).replace("  ", " ")
        logger = logging.getLogger()
        stream.write("%s %s since %s (%s)" % (
                                       Config.name.upper(),
                                       Config.version,
                                       tme,
                                       logging.getLevelName(logger.getEffectiveLevel())
                                      ))
        stream.write("\n")
        stream.flush()

    @staticmethod
    def boot(txt, stream=None, init=True):
        Kernel.privileges()
        Kernel.configure(txt)
        if stream and "v" in Config.opts:
            Kernel.banner(stream)
        Kernel.scanner(Mods.list())
        if init:
            Kernel.init(Config.sets.init or Mods.list(), "w" in Config.opts)

    @staticmethod
    def configure(txt):
        Methods.parse(Config, txt)
        Logging.level(Config.sets.level or "info")
        Workdir.configure(Config.name)
        Mods.configure()

    @staticmethod
    def forever():
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break

    @staticmethod
    def init(names, wait=False):
        thrs = []
        for name in Utils.spl(names):
            mod = Mods.get(name)
            if "init" not in dir(mod):
                continue
            thrs.append(Threads.launch(mod.init))
        if wait:
            for thr in thrs:
                thr.join()

    @staticmethod
    def privileges():
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @staticmethod
    def scanner(names):
        for mod in Mods.mods(names):
            Commands.scan(mod)
