# This file is placed in the Public Domain.


"in the beginning"


import threading
import time
import _thread


from .clients import Broker, Client
from .command import Commands
from .configs import Main
from .default import Event
from .package import Mods
from .persist import Workdir
from .require import Cmd
from .tasking import Task
from .utility import MD5, Log, Logging, Utils


logger = Log(__name__)


class Boot:

    "at startup"

    running = Event()
    stopped = Event()

    @classmethod
    def banner(cls, force=False):
        "hello."

    @classmethod
    def boot(cls):
        "prepare for runtime."
        cls.configure()
        Mods.configure()
        MD5.core()
        if Main.verbose:
            cls.banner()
        if Main.all:
            Main.mods = ",".join(Mods.list())
        Commands.table()
        Mods.table()
        if Main.scanner:
            Commands.scanner()
        Commands.add(Cmd.cmd)

    @classmethod
    def configure(cls, wdr=""):
        "setup basic variables"
        Workdir.wdr = wdr or Main.wdr or Workdir.wdr or Workdir.home(Main.name)
        Workdir.skel()
        Main.level = Main.level or "warning"
        Logging.size(len(Main.name))
        Logging.level(Main.level)

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        cls.running.set()
        while cls.running.is_set():
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break
        cls.stopped.set()

    @classmethod
    def init(cls, names, wait=False):
        "call init of modules that have an init function."
        thrs = []
        for name in Utils.spl(names):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Task.start(mod.init, name=f"init {name}"))
        if thrs and wait:
            for thr in thrs:
                thr.join()
        return True

    @classmethod
    def shutdown(cls, wait=True):
        "call stop on clients."
        logger.info("shutdown")
        for client in Broker.objs("wait"):
            logger.debug("wait %s", client)
            try:
                client.wait()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        for client in Broker.objs("stop"):
            logger.debug("stop %s", client)
            try:
                client.stop()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        if wait:
            while True:
                if len(threading.enumerate()) <= 1:
                    break
                time.sleep(0.01)
        cls.stopped.set()

    @classmethod
    def wrapped(cls, func, *args):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Client.block.set()
            _thread.interrupt_main()

    @classmethod
    def wrap(cls, func, *args, dofinal=None):
        "restore console."
        import sys
        import termios
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            old = None
        try:
            cls.wrapped(func, *args)
        except (KeyboardInterrupt, EOFError):
            pass
        if old and old[0]:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
        if dofinal:
            dofinal()


class Daemon:

    "detach from console"

    @classmethod
    def daemon(cls):
        "run in the background."
        import os
        import sys
        pid = os.fork()
        if pid != 0:
            os._exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 != 0:
            os._exit(0)
        if not Main.verbose:
            cls.null(sys.stdin)
            cls.null(sys.stdout)
            cls.null(sys.stderr)
        os.umask(0o077)
        if not Main.nochdir:
            os.chdir("/")
        os.nice(10)

    @classmethod
    def null(cls, iostream):
        "route to /dev/null."
        import os
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), iostream.fileno())

    @classmethod
    def pid(cls):
        "return pid path."
        return Workdir.pid(Main.name)

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import os
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)


def __dir__():
    return (
        'Boot',
        'Daemon'
    )
