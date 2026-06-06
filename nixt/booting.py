# This file is placed in the Public Domain.


"main"


import logging
import os
import readline
import sys
import time
import _thread


from .command import Commands
from .configs import Main
from .package import Mods
from .persist import Workdir
from .utility import Logging, Md5


class Boot:

    @classmethod
    def banner(cls):
        "hello"
        tme = time.ctime(time.time()).replace("  ", " ")
        txt = "%s %s since %s %s (%s)" % (
            Main.name.upper(),
            Main.version,
            tme,
            Main.level.upper() or "INFO",
            Md5.core()
        )
        print(txt.replace("  ", " "))
        sys.stdout.flush()

    @classmethod
    def configure(cls, cfg):
        "configure program."
        Workdir.wdr = cfg.path or os.path.expanduser(f"~/.{cfg.name}")
        Mods.add("modules", Workdir.moddir())
        if cfg.user:
            Mods.add("mods", "mods")
            Mods.add("other", "other")
        Logging.size(len(cfg.name))
        Logging.level(cfg.level or "info")

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
                time.sleep(0.01)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @classmethod
    def table(cls):
        if not Mods.table():
            logging.debug("running scanner")
            Commands.scanner()

    @classmethod
    def wrap(cls, func, *args, final=None):
        "restore console."
        import termios
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            old = False
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            print("")
        except Exception as ex:
            logging.exception(ex)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
        if final:
            final()
        readline.set_completer(None)

    pid = Workdir.pid


def __dir__():
    return (
        'Boot',
    )
