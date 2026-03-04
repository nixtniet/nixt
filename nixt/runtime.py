# This file is placed in the Public Domain.


"rutime"


import logging
import os
import sys
import time


from .command import Commands
from .configs import Main
from .defines import StaticMethod
from .objects import Dict, Methods
from .package import Mods
from .persist import Workdir
from .threads import Thread
from .utility import Log


class Runtime(StaticMethod):

    def banner():
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        print("%s %s since %s (%s)" % (
            Main.name.upper(),
            Main.version,
            tme,
            Main.level.upper(),
        ))
        sys.stdout.flush()
        return Main.version

    def boot(args, *pkgs):
        "in the beginning."
        Methods.parse(Main, args.txt)
        Dict.update(Main, Main.sets)
        Dict.merge(Main, vars(args))
        Workdir.setwd(Main.wdr)
        Log.level(Main.level or "info")
        if Main.noignore:
            Main.ignore = ""
        if Main.wdr:
            Mods.add("modules", os.path.join(Main.wdr, "mods"))
        for pkg in pkgs:
            Mods.add(pkg.__name__, pkg.__path__[0])
        if Main.local:
            Mods.add('mods', 'mods')
        if Main.verbose:
            Runtime.banner()
        if Main.all:
            Main.mods = Mods.list(Main.ignore)

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
        if cfg.wait:
            for name, thr in thrs:
                thr.join()

    def out(txt):
        print(txt.encode('utf-8', 'replace').decode("utf-8"))

    def privileges():
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    def scanner(cfg, default=True):
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

    def shutdown():
        "call shutdown on modules."
        logging.debug("shutdown")
        for mod in Dict.values(Mods.modules):
            if "shutdown" in dir(mod):
                try:
                    mod.shutdown()
                except Exception as ex:
                    logging.exception(ex)

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


SYSTEMD = """[Unit]
Description=%s
After=multi-user.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


def __dir__():
    return (
        'SYSTEMD',
        'Runtime'
    )
