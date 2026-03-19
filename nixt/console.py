# This file is placed in the Public Domain.


"main program"


import argparse
import os
import sys
import time


from .command import Commands
from .defines import Main
from .handler import Console, Event
from .objects import Dict, Methods
from .package import Mods
from .persist import Workdir
from .runtime import Runtime
from .utility import Log, Utils


from . import modules as MODS


TXT = " ".join(sys.argv[1:])


Main.level = "info"
Main.local = True
Main.name = "nixt"
Main.version = "453"


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
    def check(opts):
        for arg in sys.argv[1:]:
            if not arg.startswith("-"):
                continue
            for opt in opts:
                if opt in arg:
                    return True
        return False

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
    def background():
        "background script."
        Runtime.daemon(Main.verbose, Main.nochdir)
        Runtime.privileges()
        Runtime.boot(TXT, MODS)
        Workdir.pidfile(Main.name)
        Runtime.init(Main)
        Runtime.forever()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Runtime.boot(TXT, MODS)
        if Main.verbose:
            Run.banner()
        Runtime.init(Main, default=False)
        csl = CSL()
        csl.start()
        Runtime.forever()

    @staticmethod
    def control():
        "cli script."
        if len(sys.argv) == 1:
            return
        Main.all = True
        Runtime.boot(TXT, MODS)
        Main.mods = Mods.list(Main.ignore)
        Run.cmd(TXT)

    @staticmethod
    def service():
        "service script."
        Runtime.privileges()
        Runtime.boot(TXT, MODS)
        Run.banner()
        Workdir.pidfile(Main.name)
        Runtime.init(Main)
        Runtime.forever()


class Arguments:

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
        parser.add_argument("-r", "--read", action="store_true", help="read modules on start")
        parser.add_argument("-s", "--service", action="store_true", help="start service")
        parser.add_argument("-t", "--threaded", action='store_true', help='enable multiple workers')
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start')
        parser.add_argument("--local", action="store_true", help="use local mods directory")
        parser.add_argument("--wdr", help='set working directory')
        return parser.parse_known_args()


def main():
    "main"
    args, arguments = Arguments.getargs()
    TXT = " ".join(arguments)
    Methods.merge(Main, vars(args))
    if Main.daemon:
        Scripts.background()
    elif Main.console:
        Runtime.wrap(Scripts.console)
    elif Main.service:
        Runtime.wrap(Scripts.service)
    else:
        Runtime.wrap(Scripts.control)
    Runtime.shutdown()


if __name__ == "__main__":
    main()
