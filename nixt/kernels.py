# This file is placed in the Public Domain.


"kernel"


import os
import logging
import sys
import time
import _thread


from .command import Commands
from .configs import Main
from .objects import Data, Methods
from .package import Mods
from .persist import Disk, Workdir
from .threads import Thread
from .utility import Log, Utils


class Kernel:

    cfg = Main
    inits = []

    @classmethod
    def banner(cls):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        print("%s %s since %s %s (%s)" % (
            cls.cfg.name.upper(),
            cls.cfg.version,
            tme,
            cls.cfg.level.upper(),
            Utils.md5sum(Mods.path("tbl") or "")[:7],
        ))
        sys.stdout.flush()
        return cls.cfg.version


    @classmethod
    def boot(cls, args, *pkgs):
        "in the beginning."
        Methods.parse(cls.cfg, args.txt)
        Methods.merge(cls.cfg, cls.cfg.sets)
        Methods.merge(cls.cfg, vars(args))
        Kernel.load()
        Workdir.setwd(cls.cfg.wdr)
        Log.level(cls.cfg.level or "info")
        if cls.cfg.noignore:
            cls.cfg.ignore = ""
        if cls.cfg.user:
            Mods.add('mods', 'mods')
        if pkgs:
            for pkg in pkgs:
                Mods.pkg(pkg)
        if cls.cfg.wdr:
            Mods.add("modules", os.path.join(cls.cfg.wdr, "mods"))
        if cls.cfg.read:
            cls.scanner()
        else:
            Commands.table()
            Mods.sums()
        if cls.cfg.all:
            cls.cfg.mods = Mods.list(cls.cfg.ignore)
        if not Commands.names:
            cls.scanner()

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
                _thread.interrupt_main()

    @classmethod
    def init(cls, default=True):
        "scan named modules for commands."
        thrs = []
        if default:
            defs = cls.cfg.default
        else:
            defs = ""
        for name, mod in Mods.iter(cls.cfg.mods or defs, cls.cfg.ignore):
            if "init" in dir(mod):
                thrs.append((name, Thread.launch(mod.init)))
                cls.inits.append(name)
        if cls.cfg.wait:
            for name, thr in thrs:
                thr.join()

    @classmethod
    def load(cls):
        parsed = Data()
        Disk.read(parsed, "kernel", "config")
        Methods.merge(cls.cfg, parsed)

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @classmethod
    def save(cls):
        Disk.write(cls.cfg, "kernel", "config")

    @classmethod
    def scanner(cls, default=False):
        "scan named modules for commands."
        res = []
        if default:
            defs = cls.cfg.default
        else:
            defs = ""
        for name, mod in Mods.iter(cls.cfg.mods or defs or Mods.list(), cls.cfg.ignore):
            Commands.scan(mod)
            if "configure" in dir(mod):
                mod.configure()
            res.append((name, mod))
        return res

    @classmethod
    def shutdown(cls):
        "call shutdown on modules."
        for name in cls.inits:
            mod = Mods.get(name)
            if "shutdown" in dir(mod):
                try:
                    mod.shutdown()
                except Exception as ex:
                    logging.exception(ex)
        cls.save()

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
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as ex:
            logging.exception(ex)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def __dir__():
    return (
        "Kernel",
        'Main'
    )
