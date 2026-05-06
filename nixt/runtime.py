# This file is placed in the Public Domain.


"nixt"


import argparse
import os
import sys
import time


from .defines import Boot, Commands, Console, Method, Event, Log
from .defines import Main, Mods, Parse, Utils, Workdir


class Arguments:

    args = None
    txt = None

    @classmethod
    def getargs(cls):
        "parse commandline arguments."
        theparser = argparse.ArgumentParser(
                                         prog=Main.name,
                                         description=f'{Main.name.upper()}',
                                         epilog='use "%(prog)s cmd" for a list of commands.',
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         usage='''%(prog)s [-c|d|h|s] [-a] [-v] [-u] [-l level] [-m m1,m2] [-w] [--default] [--wdr]\n       %(prog)s [cmd] [arg=val] [arg==val]'''
                                        )
        group = theparser.add_mutually_exclusive_group()
        group.add_argument("-c", "--console", action="store_true", help="run as console.")
        group.add_argument("-d", "--daemon", action="store_true", help="run as background daemon.")
        group.add_argument("-s", "--service", action="store_true", help="run as service.")
        parser = theparser.add_argument_group()
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-l", "--level", default=Main.level, help='set loglevel.', metavar="level")
        parser.add_argument("-m", "--mods", default="", help='modules to load.', metavar="m1,m2")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start.')
        parser.add_argument("-u", "--user", action="store_true", help="use local mods directory.")
        optparser = theparser.add_argument_group()
        optparser.add_argument("--default", default="irc,rss", help="set default modules.")
        optparser.add_argument("--wdr", default="", help='set working directory.', metavar="wdr")
        args, arguments = theparser.parse_known_args()
        Main.otxt = txt = " ".join(arguments)
        Method.update(Main, args)
        Parse.parse(Main, txt)


class Line(Console):

    @staticmethod
    def cmd(text):
        "do a command."
        cli = Line()
        for txt in text.split(" ! "):
            evt = Event()
            evt.kind = "command"
            evt.orig = repr(cli)
            evt.text = txt
            Commands.command(evt)
            evt.wait()

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


class Runs:

    @classmethod
    def banner(cls):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        txt = "%s %s since %s %s (%s)" % (
            Main.name.upper(),
            Main.version,
            tme,
            Main.level.upper() or "warning",
            Boot.md5s().upper()
        )
        print(txt.replace("  ", " "))
        sys.stdout.flush()

    @classmethod
    def configure(cls):
        Main.name = Utils.pkgname(Arguments)
        Mods.add(f"{Utils.pkgname(Utils)}.modules", Utils.moddir())
        if Main.user:
            Mods.add("mods", "mods")
            Mods.add("other", "other")
        if Main.all:
            Main.mods = Mods.list()
        Log.size(len(Main.name))
        Log.level(Main.level or "warning")
        Workdir.wdr = Main.wdr or Workdir.wdr or os.path.expanduser(f"~/.{Utils.pkgname(Arguments)}")


class Scripts:

    @staticmethod
    def background():
        "background script."
        Runs.configure()
        Boot.daemon()
        Boot.privileges()
        Boot.pidfule(Main.name)
        Boot.table()
        Boot.init(Main.mods or Main.default)
        Boot.forever()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Runs.configure()
        Runs.banner()
        Boot.table()
        Boot.init(Main.mods, Main.wait)
        csl = CSL()
        csl.start()
        Boot.forever()

    @staticmethod
    def control():
        "cli script."
        Runs.configure()
        Boot.table()
        Line.cmd(Main.otxt)

    @staticmethod
    def service():
        "service script."
        Runs.configure()
        Boot.privileges()
        Boot.pidfule(Main.name)
        Boot.table()
        Runs.banner()
        Boot.init(Main.mods or Main.default)
        Boot.forever()


def main():
    "main"
    Arguments.getargs()
    if Main.daemon:
        Boot.wrap(Scripts.background)
    elif Main.console:
        Boot.wrap(Scripts.console)
    elif Main.service:
        Boot.wrap(Scripts.service)
    else:
        Boot.wrap(Scripts.control)


if __name__ == "__main__":
    main()
