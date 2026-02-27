# This file is placed in the Public Domain.


"main program"


import argparse
import logging
import os
import sys
import time


from .command import Commands
from .clients import Console
from .message import Message
from .objects import Dict, Methods, Statics
from .package import Mods
from .persist import Disk, Locate, Main, Workdir
from .threads import Thread
from .utility import Log, Utils


from . import modules as MODS


Main.default = "irc,mdl,rss,wsd"
Main.ignore = "man,rst,udp,web"
Main.version = 455
Main.wdr = os.path.expanduser(f"~/.{Main.name}")


class Line(Console):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def raw(self, text):
        "write to console."
        Runtime.out(text)


class CSL(Line):

    def callback(self, event):
        "wait for callback result."
        if not event.text:
            event.ready()
            return
        super().callback(event)
        event.wait()

    def poll(self):
        "poll for an event."
        evt = Message()
        evt.text = input("> ")
        evt.kind = "command"
        return evt


class Runtime(Statics):
    
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

    def boot(args):
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
        if MODS:
            Mods.add(MODS.__name__, MODS.__path__[0])
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

    def getargs():
        "parse commandline arguments."
        parser = argparse.ArgumentParser(prog=Main.name, description=f"{Main.name.upper()}")
        parser.add_argument("-a", "--all", action="store_true", help="load all modules")
        parser.add_argument("-c", "--console", action="store_true", help="start console")
        parser.add_argument("-d", "--daemon", action="store_true", help="start background daemon")
        parser.add_argument("-l", "--level", default=Main.level, help='set loglevel')
        parser.add_argument("-m", "--mods", default="", help='modules to load')
        parser.add_argument("-n", "--noignore", action="store_true", help="disable ignore")
        parser.add_argument("-s", "--service", action="store_true", help="start service")
        parser.add_argument("-v", "--verbose", action='store_true',help='enable verbose')
        parser.add_argument("-w", "--wait", action='store_true',help='wait for services to start')
        parser.add_argument("--local", action="store_true", help="use local mods directory")
        parser.add_argument("--wdr", help='set working directory')
        return parser.parse_known_args()

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
                mod.configure(cfg)
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


class Scripts(Statics):

    def background(args):
        "background script."
        Runtime.daemon(Main.verbose, Main.nochdir)
        Runtime.privileges()
        Runtime.boot(args)
        Workdir.pidfile(Main.name)
        Runtime.scanner(Main)
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Runtime.init(Main)
        Utils.forever()

    def console(args):
        "console script."
        import readline
        readline.redisplay()
        Runtime.boot(args)
        Runtime.scanner(Main, False)
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Commands.cmd(Main.txt)
        Runtime.init(Main, default=False)
        csl = CSL()
        csl.start()
        Utils.forever()

    def control(args):
        "cli script."
        if len(sys.argv) == 1:
            return
        Runtime.boot(args)
        Main.mods = Mods.list(Main.ignore)
        Runtime.scanner(Main)
        Commands.add(Cmd.cfg, Cmd.cmd, Cmd.mod, Cmd.srv, Cmd.ver)
        evt = Commands.cmd(Main.txt)
        for line in evt.result.values():
            Runtime.out(line)

    def service(args):
        "service script."
        Runtime.privileges()
        Runtime.banner()
        Runtime.boot(args)
        Workdir.pidfile(Main.name)
        Runtime.scanner(Main)
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Runtime.init(Main)
        Utils.forever()


class Cmd(Statics):

    def cfg(event):
        if not event.args:
            event.reply(f"cfg <{Mods.has('Config') or 'modulename'}>")
            return
        name = event.args[0]
        mod = Mods.get(name)
        if not mod:
            event.reply(f"no {name} module found.")
            return
        cfg = getattr(mod, "Config", None)
        if not cfg:
            event.reply("no configuration found.")
            return
        fnm = Locate.first(cfg) or Methods.ident(cfg)
        if not event.sets:
            event.reply(
                Methods.fmt(
                    cfg,
                    Dict.keys(cfg),
                    skip=["word",]
                )
            )
            return
        Methods.edit(cfg, event.sets)
        Disk.write(Methods.skip(cfg), fnm)
        event.reply("ok")

    def cmd(event):
        "list available commands."
        event.reply(",".join(sorted(Commands.names or Commands.cmds)))

    def mod(event):
        "list available commands."
        mods = Mods.list(Main.ignore)
        if not mods:
            event.reply("no modules available")
            return
        event.reply(mods)

    def srv(event):
        "generate systemd service file."
        import getpass
        name = getpass.getuser()
        event.reply(SYSTEMD % (Main.name.upper(), name, name, name, Main.name))

    def ver(event):
        "show verson."
        event.reply(f"{Main.name.upper()} {Main.version}")


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


def main():
    "main"
    args, arguments = Runtime.getargs()
    args.txt = " ".join(arguments)
    if args.daemon:
        Scripts.background(args)
    elif args.console:
        Runtime.wrap(Scripts.console, args)
    elif args.service:
        Runtime.wrap(Scripts.service, args)
    else:
        Runtime.wrap(Scripts.control, args)
    Runtime.shutdown()
