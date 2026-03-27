# This file is placed in the Public Domain.


"main program"


import argparse
import os
import sys
import time


from .command import Commands
from .configs import Main
from .kernels import Kernel
from .handler import Console, Event
from .objects import Methods
from .package import Mods
from .persist import Workdir
from .utility import Log, Utils


from . import modules as MODS


Kernel.cfg.level = "info"
Kernel.cfg.version = "453"
Kernel.cfg.wdr = os.path.expanduser(f"~/.{Main.name}")


class Arguments:

    @staticmethod
    def getargs():
        "parse commandline arguments."
        parser = argparse.ArgumentParser(prog=Kernel.cfg.name, description=f"{Kernel.cfg.name.upper()}")
        parser.add_argument("-a", "--all", action="store_true", help="load all modules")
        parser.add_argument("-c", "--console", action="store_true", help="start console")
        parser.add_argument("-d", "--daemon", action="store_true", help="start background daemon")
        parser.add_argument("-i", "--ignore", default="", help='modules to ignore')
        parser.add_argument("-l", "--level", default=Kernel.cfg.level, help='set loglevel')
        parser.add_argument("-m", "--mods", default="", help='modules to load')
        parser.add_argument("-n", "--noignore", action="store_true", help="disable ignore")
        parser.add_argument("-r", "--read", action="store_true", help="read modules on start")
        parser.add_argument("-s", "--service", action="store_true", help="start service")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start')
        parser.add_argument("-u", "--user", action="store_true", help="use local mods directory")
        parser.add_argument("-wdr", "--wdr", default="", help='set working directory')
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
        Kernel.daemon(Main.verbose, Main.nochdir)
        Kernel.privileges()
        Kernel.boot(args, MODS)
        Workdir.pidfile(Main.name)
        Kernel.init()
        Kernel.forever()

    @staticmethod
    def console(args):
        "console script."
        import readline
        readline.redisplay()
        Kernel.boot(args, MODS)
        if Kernel.cfg.verbose:
            Kernel.banner()
        Kernel.init(default=False)
        csl = CSL()
        csl.start()
        Kernel.forever()

    @staticmethod
    def control(args):
        "cli script."
        if len(sys.argv) == 1:
            return
        Kernel.cfg.all = True
        Kernel.boot(args, MODS)
        Kernel.cfg.mods = Mods.list(Kernel.cfg.ignore)
        Run.cmd(args.txt)

    @staticmethod
    def service(args):
        "service script."
        Kernel.privileges()
        Kernel.boot(args, MODS)
        Kernel.banner()
        Workdir.pidfile(Main.name)
        Kernel.init()
        Kernel.forever()


def main():
    "main"
    args, arguments = Arguments.getargs()
    args.txt = " ".join(arguments)
    if args.daemon:
        Scripts.background(args)
    elif args.console:
        Kernel.wrap(Scripts.console, args)
    elif args.service:
        Kernel.wrap(Scripts.service, args)
    else:
        Kernel.wrap(Scripts.control, args)
    Kernel.shutdown()


if __name__ == "__main__":
    main()
