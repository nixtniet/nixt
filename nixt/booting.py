# This file is placed in the Public Domain.


"in the beginning"


import argparse
import logging
import os
import pathlib
import sys
import time
import _thread


from .brokers import Broker
from .command import Commands
from .configs import Main
from .handler import Console, Event
from .objects import Object
from .package import Mods
from .persist import Disk, Workdir
from .threads import Thread
from .utility import Log, Utils


class Arguments:

    args = None
    txt = None

    @classmethod
    def getargs(cls):
        "parse commandline arguments."
        parser = argparse.ArgumentParser(prog=Main.name, description=f"{Main.name.upper()}")
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-c", "--console", action="store_true", help="start console.")
        parser.add_argument("-d", "--background", action="store_true", help="start background daemon.")
        parser.add_argument("-i", "--ignore", default="", help='modules to ignore.')
        parser.add_argument("-l", "--level", default=Main.level, help='set loglevel.')
        parser.add_argument("-m", "--mods", default="", help='modules to load.')
        parser.add_argument("-n", "--index", action="store", type=int, help="set index to use.")
        parser.add_argument("-p", "--prune", action="store_true", help="prune directories.")
        parser.add_argument("-r", "--read", action="store_true", help="read modules on start.")
        parser.add_argument("-s", "--service", action="store_true", help="start service.")
        parser.add_argument("-t", "--threaded", action="store_true", help="use threads.")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start.')
        parser.add_argument("-u", "--user", action="store_true", help="use local mods directory.")
        parser.add_argument("-x", "--admin", action="store_true", help="enable admin mode.")
        parser.add_argument("--wdr", help='set working directory.')
        parser.add_argument("--nochdir", action="store_true", help='set working directory.')
        cls.args, arguments = parser.parse_known_args()
        cls.txt = " ".join(arguments)
        Object.merge(Main, cls.args)


class Line(Console):

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class CSL(Line):

    def poll(self):
        "poll for an event."
        evt = Event()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        return evt


class Kernel:

    configured = False
    inits = []
    md5s = {}
    path = os.path.dirname(__spec__.loader.path)

    @classmethod
    def banner(cls):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        print("%s since %s %s (%s)" % (
            Main.name.upper(),
            tme,
            Main.level.upper() or "INFO",
            Utils.md5sum(Mods.path("tbl") or "")[:7],
        ))
        sys.stdout.flush()

    @classmethod
    def boot(cls):
        Arguments.getargs()
        csl = None
        if Arguments.txt:
            Boot.cmd(" ".join(sys.argv[1:]))
            return
        if Main.console:
            import readline
            readline.redisplay()
            csl = CSL()
        elif Main.daemon:
            cls.daemon()
        if Main.daemon or Main.service:
            cls.privileges()
        cls.configure()
        if Main.verbose:
            cls.banner()
        if Main.daemon or Main.service:
            cls.pidfile(Main.name)
        cls.scan()
        if Main.all or Main.mods:
            cls.init()
        if csl:
            csl.start()
        if Main.daemon or Main.service or Main.console:
            cls.forever()
        cls.shutdown()

    @classmethod
    def cmd(cls, text):
        cli = Line()
        for txt in text.split(" ! "):
            evt = Event()
            evt.kind = "command"
            evt.orig = repr(cli)
            evt.text = txt
            Commands.command(evt)
            evt.wait()
        return evt

    @classmethod
    def configure(cls, name=""):
        "in the beginning."
        if cls.configured:
            return
        Main.name = name or Main.name or Utils.pkgname(Boot)
        if Main.read:
            Disk.read(Main, "main", "config")
        if Main.wdr == f".{Main.name}":
            Main.wdr = os.path.expanduser(f"~/.{Main.name}")
        cls.md5s.update(Utils.md5dir(cls.path))
        Workdir.skel()
        Log.size(len(Main.name))
        Log.level(Main.level or "info")
        if Main.user:
            Mods.add(os.path.join(Main.wdr, "mods"), "modules")
            Mods.add('mods', 'mods')
        if Main.all:
            Main.mods = Mods.list()
        cls.configured = True

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
        for name, mod in Mods.iter():
            if "init" in dir(mod):
                thrs.append((name, Thread.launch(mod.init)))
                cls.inits.append(name)
        if Main.wait:
            for name, thr in thrs:
                thr.join()

    @staticmethod
    def pidfile(name):
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
        for name, mod in Mods.iter():
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
        Broker.stop()

    @classmethod
    def start(cls):
        cls.wrap(cls.boot)

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
