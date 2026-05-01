# This file is placed in the Public Domain.


"in the beginning"


import logging
import os
import sys
import time


from .command import Commands
from .configs import Main
from .objects import Object
from .package import Mods
from .persist import Disk, Workdir
from .threads import Thread
from .utility import Log, Utils


class Boot:

    inits = []

    @classmethod
    def banner(cls):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        print("%s since %s %s (%s)" % (
            Main.name.upper(),
            tme,
            Main.level.upper() or "warning",
            cls.md5s().upper()
        ))
        sys.stdout.flush()

    @classmethod
    def configure(cls, cfg):
        "in the beginning."
        Workdir.configure(cfg)
        if cfg.read:
            Disk.read(Main, "main", "config")
        Log.configure(cfg)
        Mods.configure(cfg)
        if cfg.noignore:
            cfg.ignore = ""
        if not cfg.mods:
            cfg.mods = Mods.list(cfg.ignore)
        if cfg.all:
            cfg.init = Mods.list(cfg.ignore)
        if cfg.daemon or cfg.service:
            Workdir.pidfile(cfg.name)

    @classmethod
    def daemon(cls, verbose=False, nochdir=False):
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

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break

    @classmethod
    def init(cls, cfg):
        "scan named modules for commands."
        thrs = []
        for name, mod in Mods.iter(cfg.init, cfg.ignore):
            if "init" in dir(mod):
                thrs.append((name, Thread.launch(mod.init)))
                cls.inits.append(name)
        if not cfg.nowait:
            for name, thr in thrs:
                thr.join()

    @classmethod
    def md5s(cls):
        paths = []
        paths.append(os.path.dirname(__spec__.loader.path))
        for path in Object.values(Mods.dirs):
            paths.append(path)
        return str(Utils.md5s(*paths)[:7])

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @classmethod
    def scanner(cls, cfg):
        "scan named modules for commands."
        for name, mod in Mods.iter(cfg.mods, cfg.ignore):
            Commands.scan(mod)
            if "configure" in dir(mod):
                mod.configure()

    @classmethod
    def shutdown(cls):
        "call shutdown on modules."
        for name in cls.inits:
            mod = Mods.get(name)
            if "shutdown" in dir(mod):
                mod.shutdown()

    @classmethod
    def wrap(cls, func, *args):
        "restore console."
        import termios
        old = None
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            pass
        try:
            func(*args)
            cls.shutdown()
        except (KeyboardInterrupt, EOFError):
            os._exit(0)
        except Exception as ex:
            logging.exception(ex)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def __dir__():
    return (
        "Boot",
    )
