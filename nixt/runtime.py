# This file is placed in the Public Domain.


"main program"


import argparse
import os
import sys
import time


from .command import Commands
from .configs import Main
from .daemons import Runtime
from .handler import Console, Event
from .objects import Methods
from .package import Mods
from .persist import Workdir
from .utility import Log, Utils


from . import modules as MODS


Main.level = "info"
Main.version = "453"
Main.wdr = os.path.expanduser(f"~/.{Main.name}")


class Arguments:

    @staticmethod
    def getargs():
        "parse commandline arguments."
        parser = argparse.ArgumentParser(prog=Main.name, description=f"{Main.name.upper()}")
        parser.add_argument("-a", "--all", action="store_true", help="load all modules")
        parser.add_argument("-b", "--background", action="store_true", help="start background daemon")
        parser.add_argument("-c", "--console", action="store_true", help="start console")
        parser.add_argument("-d", "--wdr", default="", help='set working directory')
        parser.add_argument("-i", "--ignore", default="", help='modules to ignore')
        parser.add_argument("-l", "--level", default=Main.level, help='set loglevel')
        parser.add_argument("-m", "--mods", default="", help='modules to load')
        parser.add_argument("-n", "--noignore", action="store_true", help="disable ignore")
        parser.add_argument("-r", "--read", action="store_true", help="read modules on start")
        parser.add_argument("-s", "--service", action="store_true", help="start service")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start')
        parser.add_argument("-u", "--user", action="store_true", help="use local mods directory")
        return parser.parse_known_args()


class Line(Console):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


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


class Run:

    @staticmethod
    def banner():
        "hello."
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
        Methods.merge(Main, Main.sets)
        Methods.merge(Main, vars(args))
        Workdir.setwd(Main.wdr)
        Log.level(Main.level or "info")
        if Main.noignore:
            Main.ignore = ""
        if Main.user:
            Mods.add('mods', 'mods')
        if pkgs:
            for pkg in pkgs:
                Mods.pkg(pkg)
        if Main.wdr:
            Mods.add("modules", os.path.join(Main.wdr, "mods"))
        if Main.read:
            Runtime.scanner(Main)
        else:
            Commands.table()
            Mods.sums()
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


class Scripts:

    @staticmethod
    def background(args):
        "background script."
        Runtime.daemon(Main.verbose, Main.nochdir)
        Runtime.privileges()
        Run.boot(args, MODS)
        Workdir.pidfile(Main.name)
        Runtime.init(Main)
        Runtime.forever()

    @staticmethod
    def console(args):
        "console script."
        import readline
        readline.redisplay()
        Run.boot(args, MODS)
        if Main.verbose:
            Run.banner()
        Runtime.init(Main, default=False)
        csl = CSL()
        csl.start()
        Runtime.forever()

    @staticmethod
    def control(args):
        "cli script."
        if len(sys.argv) == 1:
            return
        Main.all = True
        Run.boot(args, MODS)
        Main.mods = Mods.list(Main.ignore)
        Run.cmd(args.txt)

    @staticmethod
    def service(args):
        "service script."
        Runtime.privileges()
        Run.boot(args, MODS)
        Run.banner()
        Workdir.pidfile(Main.name)
        Runtime.init(Main)
        Runtime.forever()


def main():
    "main"
    args, arguments = Arguments.getargs()
    args.txt = " ".join(arguments)
    if args.background:
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
