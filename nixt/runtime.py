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


TXT = " ".join(sys.argv[1:])


Main.level = "warning"
Main.version = "453"
Main.wdr = os.path.expanduser(f"~/.{Main.name}")


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
    def check(opts):
        for word in TXT.split():
            if not word.startswith("-"):
                continue
            for char in opts:
                if char in word:
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
        Kernel.daemon(Main.verbose, Main.nochdir)
        Kernel.privileges()
        Kernel.boot(TXT, MODS)
        Workdir.pidfile(Main.name)
        Kernel.init()
        Kernel.forever()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Kernel.boot(TXT, MODS)
        Kernel.init(default=False)
        csl = CSL()
        csl.start()
        Kernel.forever()

    @staticmethod
    def control():
        "cli script."
        if len(sys.argv) == 1:
            return
        Main.all = True
        Kernel.boot(TXT, MODS)
        Main.mods = Mods.list(Main.ignore)
        Run.cmd(TXT)

    @staticmethod
    def service():
        "service script."
        Kernel.privileges()
        Kernel.boot(TXT, MODS)
        Workdir.pidfile(Main.name)
        Kernel.init()
        Kernel.forever()


check = Run.check


def main():
    "main"
    if check('a'): Main.all = True
    if check('n'): Main.noignore = True
    if check('r'): Main.read = True
    if check("u"): Main.user = True
    if check("v"): Main.verbose = True
    if check("w"): Main.wait = True
    if check("d"): Scripts.background()
    elif check("c"): Kernel.wrap(Scripts.console)
    elif check("s"): Kernel.wrap(Scripts.service)
    else: Kernel.wrap(Scripts.control)
    Kernel.shutdown()


if __name__ == "__main__":
    main()
