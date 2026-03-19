# This file is placed in the Public Domain.


"runtime"


import os
import logging
import sys
import time
import _thread


from .command import Commands
from .defines import Main
from .objects import Dict, Methods
from .package import Mods
from .persist import Workdir
from .threads import Thread
from .utility import Log


class Runtime:

    inits = []

    @staticmethod
    def boot(txt, *pkgs):
        "in the beginning."
        Methods.parse(Main, txt)
        Methods.merge(Main, Main.sets)
        Workdir.setwd(Main.wdr)
        Log.level(Main.level or "info")
        if Main.noignore:
            Main.ignore = ""
        if Main.local:
            Mods.add('mods', 'mods')
        if pkgs:
            for pkg in pkgs:
                Mods.pkg(pkg)
        if Main.wdr:
            Mods.add("modules", os.path.join(Main.wdr, "mods"))
        if Main.read:
            Runtime.scanner(Main)
        else:
            Commands.table()
            Mods.sums()
        if Main.all:
            Main.mods = Mods.list(Main.ignore)
        if not Commands.names:
            Runtime.scanner(Main)

    @staticmethod
    def daemon(verbose=False, nochdir=False):
        "run in the background."
        pid = os.fork()
        if pid != 0:
            os._exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 != 0:
            os._exit(0)
        if not verbose:
            with open('/dev/null', 'r', encoding="utf-8") as sis:
                os.dup2(sis.fileno(), sys.stdin.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as sos:
                os.dup2(sos.fileno(), sys.stdout.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as ses:
                os.dup2(ses.fileno(), sys.stderr.fileno())
        os.umask(0)
        if not nochdir:
            os.chdir("/")
        os.nice(10)

    @staticmethod
    def forever():
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @staticmethod
    def init(cfg, default=True):
        "scan named modules for commands."
        thrs = []
        if default:
            defs = cfg.default
        else:
            defs = ""
        for name, mod in Mods.iter(cfg.mods or defs, cfg.ignore):
            if "init" in dir(mod):
                thrs.append((name, Thread.launch(mod.init)))
                Runtime.inits.append(name)
        if cfg.wait:
            for name, thr in thrs:
                thr.join()

    @staticmethod
    def privileges():
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @staticmethod
    def scanner(cfg, default=False):
        "scan named modules for commands."
        res = []
        if default:
            defs = cfg.default
        else:
            defs = ""
        for name, mod in Mods.iter(cfg.mods or defs or Mods.list(), cfg.ignore):
            Commands.scan(mod)
            if "configure" in dir(mod):
                mod.configure()
            res.append((name, mod))
        return res

    @staticmethod
    def shutdown():
        "call shutdown on modules."
        for name in Runtime.inits:
            mod = Mods.get(name)
            if "shutdown" in dir(mod):
                try:
                    mod.shutdown()
                except Exception as ex:
                    logging.exception(ex)

    @staticmethod
    def wrap(func, *args):
        "restore console."
        import termios
        old = None
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            pass
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as ex:
            logging.exception(ex)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)



def __dir__():
    return (
        "Runtime",
    )
