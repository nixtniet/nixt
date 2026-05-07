# This file is placed in the Public Domain.


"in the beginning"


import inspect
import logging
import os
import pathlib
import sys
import time


from .command import Commands
from .package import Mods
from .persist import Workdir
from .threads import Thread
from .utility import Utils


from . import statics


e = os.path.exists
j = os.path.join


class Boot:

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
                return

    @classmethod
    def init(cls, modlist, wait=False):
        thrs = []
        for name in Utils.spl(modlist):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Thread.launch(mod.init))
        if thrs and wait:
            for thr in thrs:
                thr.join()

    @classmethod
    def md5(cls):
        return Utils.md5source(inspect.getsource(statics))[:7].upper()

    @classmethod
    def pidfile(cls, name):
        "write pidfile."
        filename = j(Workdir.wdr, f"{name}.pid")
        if e(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @classmethod
    def scanner(cls):
        "scan named modules for commands."
        if Commands.names:
            return
        for name in Utils.spl(Mods.list()):
            mod = Mods.get(name)
            if not mod:
                continue
            Commands.scan(mod)

    @classmethod
    def table(cls):
        try:
            from .statics import NAMES, CORE, MD5
            Commands.names.update(NAMES)
            Mods.core.update(CORE)
            Mods.md5s.update(MD5)
        except ImportError:
            cls.scanner()

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
        'Boot',
    )
