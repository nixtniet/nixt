# This file is placed in the Public Domain.


"main program"


import argparse
import base64
import logging
import os
import time


from nixt.command import Commands
from nixt.defines import Main, version
from nixt.handler import Console, Event
from nixt.loggers import Log
from nixt.objects import Dict, Methods
from nixt.package import Mods
from nixt.persist import Disk, Json, Locate, Workdir
from nixt.threads import Thread
from nixt.utility import SYSTEMD, Utils


from nixt import modules as MODS


Main.default = "irc,rss,thr"
Main.ignore = "udp"
Main.level = "info"
Main.local = True
Main.version = version
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
        evt = Event()
        evt.text = input("> ")
        evt.kind = "command"
        return evt


class Runtime:

    inits = []

    @staticmethod
    def banner():
        "hello."
        import sys
        tme = time.ctime(time.time()).replace("  ", " ")
        print("%s %s since %s %s (%s)" % (
            Main.name.upper(),
            Main.version,
            tme,
            Main.level.upper(),
            Utils.md5sum(Mods.path("tbl") or "")[:7],
        ))
        sys.stdout.flush()
        return Main.version

    @staticmethod
    def boot(args, *pkgs):
        "in the beginning."
        Methods.parse(Main, args.txt)
        Dict.update(Main, Main.sets)
        Methods.merge(Main, vars(args))
        Workdir.setwd(Main.wdr)
        Log.level(Main.level or "info")
        if Main.noignore:
            Main.ignore = ""
        if pkgs:
            for pkg in pkgs:
                Mods.pkg(pkg)
        if Main.wdr:
            Mods.add("modules", os.path.join(Main.wdr, "mods"))
        if Main.local:
            Mods.add('mods', 'mods')
        Commands.table()
        Mods.sums()
        if Main.verbose:
            Runtime.banner()
        if Main.all:
            Main.mods = Mods.list(Main.ignore)
        if not Commands.names:
            Runtime.scanner(Main)

    @staticmethod
    def cmd(text):
        "parse text for command and run it."
        cli = Line()
        cli.start()
        for txt in text.split(" ! "):
            evt = Event()
            evt.orig = repr(cli)
            evt.text = txt
            evt.kind = "command"
            Commands.command(evt)
            evt.wait()
        return evt

    @staticmethod
    def daemon(verbose=False, nochdir=False):
        "run in the background."
        import sys
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

    @staticmethod
    def forever():
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break

    @staticmethod
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
        parser.add_argument("-t", "--threaded", action='store_true', help='enable multiple workers')
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start')
        parser.add_argument("--local", action="store_true", help="use local mods directory")
        parser.add_argument("--wdr", help='set working directory')
        return parser.parse_known_args()

    @staticmethod
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
                Runtime.inits.append(name)
        if cfg.wait:
            for name, thr in thrs:
                thr.join()

    @staticmethod
    def out(txt):
        print(txt.encode('utf-8', 'replace').decode("utf-8"))

    @staticmethod
    def privileges():
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @staticmethod
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

    @staticmethod
    def shutdown():
        "call shutdown on modules."
        for name in Runtime.inits:
            mod = Mods.get(name)
            if "shutdown" in dir(mod):
                try:
                    mod.shutdown()
                except Exception as ex:
                    logging.exception(ex)

    @staticmethod
    def wrap(func, *args):
        "restore console."
        import sys
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


class Scripts:

    @staticmethod
    def background(args):
        "background script."
        Runtime.daemon(Main.verbose, Main.nochdir)
        Runtime.privileges()
        Runtime.boot(args, MODS)
        Workdir.pidfile(Main.name)
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Runtime.init(Main)
        Runtime.forever()

    @staticmethod
    def console(args):
        "console script."
        import readline
        readline.redisplay()
        Runtime.boot(args, MODS)
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Runtime.init(Main, default=False)
        csl = CSL()
        csl.start()
        Runtime.forever()

    @staticmethod
    def control(args):
        "cli script."
        import sys
        if len(sys.argv) == 1:
            return
        Main.all = True
        Runtime.boot(args, MODS)
        Main.mods = Mods.list(Main.ignore)
        Commands.add(*Dict.values(Cmd))
        Runtime.cmd(Main.txt)

    @staticmethod
    def service(args):
        "service script."
        Runtime.privileges()
        Runtime.boot(args, MODS)
        Runtime.banner()
        Workdir.pidfile(Main.name)
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Runtime.init(Main)
        Runtime.forever()


class Cmd:

    @staticmethod
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

    @staticmethod
    def cmd(event):
        "list available commands."
        event.reply(",".join(sorted(Commands.names.keys() or Commands.cmds.keys())))

    @staticmethod
    def mod(event):
        "list available commands."
        mods = Mods.list(Main.ignore)
        if not mods:
            event.reply("no modules available")
            return
        event.reply(mods)

    @staticmethod
    def pwd(event):
        if len(event.args) != 2:
            event.reply("pwd <nick> <password>")
            return
        arg1 = event.args[0]
        arg2 = event.args[1]
        txt = f"\x00{arg1}\x00{arg2}"
        enc = txt.encode("ascii")
        base = base64.b64encode(enc)
        dcd = base.decode("ascii")
        event.reply(dcd)

    @staticmethod
    def srv(event):
        "generate systemd service file."
        import getpass
        name = getpass.getuser()
        event.reply(SYSTEMD % (Main.name.upper(), name, name, name, Main.name))

    @staticmethod
    def tbl(event):
        Mods.md5s = {}
        for name, mod in Mods.all():
            Commands.scan(mod)
        event.reply("# This file is placed in the Pubic Domain.\n\n")
        event.reply(f"NAMES = {Json.dumps(Commands.names, indent=4)}\n\n")
        event.reply(f"MD5 = {Json.dumps(Mods.md5s, indent=4)}")

    @staticmethod
    def ver(event):
        "show verson."
        event.reply(f"{Main.name.upper()} {Main.version}")


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


if __name__ == "__main__":
    main()
