# This file is placed in the Public Domain.


"runtime"


import os
import sys
import time


from .booting import Boot
from .command import Commands
from .configs import Main
from .handler import Console, Event
from .package import Mods
from .utility import Utils


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


class Run:

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


class Scripts:

    @staticmethod
    def background():
        "background script."
        Boot.daemon(Main.verbose, Main.nochdir)
        Boot.privileges()
        Boot.boot(read=True)
        Boot.pidfile(Main.name)
        Boot.scan()
        Boot.init()
        Boot.forever()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Boot.boot()
        if Main.verbose:
            Run.banner()
        Boot.scan()
        Boot.init()
        csl = CSL()
        csl.start()
        Boot.forever()

    @staticmethod
    def control():
        "cli script."
        if len(sys.argv) == 1:
            return
        Boot.boot(doall=True)
        Boot.scan()
        cli = Line()
        for text in Boot.txt.split(" ! "):
            evt = Event()
            evt.kind = "command"
            evt.orig = repr(cli)
            evt.text = text
            Commands.command(evt)
            evt.wait()
        return evt

    @staticmethod
    def service():
        "service script."
        Boot.privileges()
        Boot.boot(read=True)
        Boot.scan()
        Run.banner()
        Boot.pidfile(Main.name)
        Boot.init()
        Boot.forever()


check = Boot.check


def line(name=""):
    "command line interface."
    Main.name = name or Main.name
    Scripts.control()


def main(name=""):
    "main"
    Main.name = name or Main.name
    txt = " ".join(sys.argv[1:])
    if check('a', txt): Main.all = True
    if check('b', txt): Main.boot = True
    if check('n', txt): Main.noignore = True
    if check('r', txt): Main.read = True
    if check("u", txt): Main.user = True
    if check("v", txt): Main.verbose = True
    if check("w", txt): Main.wait = True
    if Main.user: Mods.add('mods', 'mods')
    if Main.wdr: Mods.add("modules", os.path.join(Main.wdr, "mods"))
    if Main.all: Main.mods = Mods.list(Main.ignore)
    if check("d", txt): Scripts.background()
    elif check("c", txt): Boot.wrap(Scripts.console)
    elif check("s", txt): Boot.wrap(Scripts.service)
    else: Boot.wrap(Scripts.control)
    Boot.shutdown()
