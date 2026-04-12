# This file is placed in the Public Domain.


"in the beginning"


import logging
import os
import pathlib
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


class Boot:

    inits = []
    md5s = {}
    txt = " ".join(sys.argv[1:])

    @classmethod
    def boot(cls, name="", read=False, doall=False):
        "in the beginning."
        Main.name = name or Main.name or Utils.pkgname(Boot)
        Main.wdr = os.path.expanduser(f"~/.{Main.name}")
        cls.core()
        if Main.boot or read:
            Disk.read(Main, "main", "config")
        else:
            Methods.parse(Main, cls.txt)
        Workdir.skel()
        Log.size(len(Main.name))
        Log.level(Main.level or "info")
        if Main.user:
            Mods.add('mods', 'mods')
        if Main.wdr:
            Mods.add("modules", os.path.join(Main.wdr, "mods"))
        if Main.all or doall:
            Main.mods = Mods.list(Main.ignore)

    @classmethod
    def check(cls, opts):
        for word in cls.txt.split():
            if not word.startswith("-"):
                continue
            for char in opts:
                if char in word:
                    return True
        return False

    @classmethod
    def core(cls):
        "calculate core md5."
        path = os.path.dirname(__spec__.loader.path)
        for fnm in os.listdir(path):
            if not fnm.endswith(".py"):
                continue
            name = fnm[:-3]
            mpath = os.path.join(path, fnm)
            cls.md5s[name] = Utils.md5sum(mpath)

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
    def init(cls):
        "scan named modules for commands."
        thrs = []
        for name, mod in Mods.iter(Main.ignore):
            if "init" in dir(mod):
                thrs.append((name, Thread.launch(mod.init)))
                cls.inits.append(name)
        if Main.wait:
            for name, thr in thrs:
                thr.join()

    @classmethod
    def pidfile(cls, name):
        "write pidfile."
        filename = os.path.join(Main.wdr, f"{name}.pid")
        if os.path.exists(filename):
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
    def scan(cls):
        if Main.read:
            cls.scanner()
        else:
            Commands.table()
            Mods.sums()
        if not Commands.names:
            cls.scanner()

    @classmethod
    def scanner(cls):
        "scan named modules for commands."
        res = []
        for name, mod in Mods.iter(Main.ignore):
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
        "Boot",
    )
