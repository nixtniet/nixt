# This file is placed in the Public Domain.


"kernel"


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


class Kernel:

    inits = []

    @classmethod
    def banner(cls):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        print("%s %s since %s %s (%s)" % (
            Main.name.upper(),
            Main.version,
            tme,
            Main.level.upper() or "INFO",
            Utils.md5sum(Mods.path("tbl") or "")[:7]
        ))
        sys.stdout.flush()
        return Main.version

    @classmethod
    def boot(cls, txt, *pkgs):
        "in the beginning."
        if Main.boot:
            cls.load()
        else:
            parsed = Data()
            Methods.parse(parsed, txt)
            Methods.merge(Main, parsed)
            Methods.merge(Main, parsed.sets)
        print(Main)
        Workdir.setwd(Main.wdr)
        Log.size(len(Main.name))
        Log.level(Main.level or "info")
        if Main.noignore: Main.ignore = ""
        if Main.user: Mods.add('mods', 'mods')
        if pkgs:
            for pkg in pkgs:
                Mods.pkg(pkg)
        if Main.wdr: Mods.add("modules", os.path.join(Main.wdr, "mods"))
        if Main.read: cls.scanner()
        else: Commands.table() ; Mods.sums()
        if Main.verbose: cls.banner()
        if Main.all: Main.mods = Mods.list(Main.ignore)
        if not Commands.names: cls.scanner()

    @classmethod
    def daemon(cls, verbose=False, nochdir=False):
        "run in the background."
        pid = os.fork()
        if pid != 0: os._exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 != 0: os._exit(0)
        if not verbose:
            with open('/dev/null', 'r', encoding="utf-8") as sis:
                os.dup2(sis.fileno(), sys.stdin.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as sos:
                os.dup2(sos.fileno(), sys.stdout.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as ses:
                os.dup2(ses.fileno(), sys.stderr.fileno())
        os.umask(0)
        if not nochdir: os.chdir("/")
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
        if default: defs = Main.default
        else: defs = ""
        for name, mod in Mods.iter(Main.mods or defs, Main.ignore):
            if "init" in dir(mod):
                thrs.append((name, Thread.launch(mod.init)))
                cls.inits.append(name)
        if Main.wait:
            for name, thr in thrs: thr.join()

    @classmethod
    def load(cls):
        logging.info("loading kernel")
        Disk.read(Main, "kernel", "config")

    @classmethod
    def pidfile(cls, name):
        "write pidfile."
        filename = os.path.join(cls.wdr, f"{name}.pid")
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
    def save(cls):
        "save kernel to disk."
        logging.info("saving kenrel")
        Disk.write(Main, "kernel", "config")

    @classmethod
    def scanner(cls, default=False):
        "scan named modules for commands."
        res = []
        if default: defs = Main.default
        else: defs = ""
        for name, mod in Mods.iter(Main.mods or defs or Mods.list(), Main.ignore):
            Commands.scan(mod)
            if "configure" in dir(mod): mod.configure()
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
        try: old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error: pass
        try: func(*args)
        except (KeyboardInterrupt, EOFError): pass
        except Exception as ex: logging.exception(ex)
        if old: termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def __dir__():
    return (
        "Kernel",
    )
