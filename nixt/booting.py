# This file is placed in the Public Domain.


"at the beginning"


import argparse


from .runtime import Runtime
from .command import Commands
from .configs import Main
from .handler import Console, Event
from .objects import Object


class Arguments:

    args = None
    txt = None

    @classmethod
    def getargs(cls):
        "parse commandline arguments."
        parser = argparse.ArgumentParser(prog=Main.name, description=f"{Main.name.upper()}")
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-c", "--console", action="store_true", help="start console.")
        parser.add_argument("-d", "--daemon", action="store_true", help="start background daemon.")
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
        parser.add_argument("--noignore", action="store_true", help="disable ignore")
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


class Scripts:

    @staticmethod
    def background():
        "background script."
        Runtime.daemon(Main.verbose, Main.nochdir)
        Runtime.privileges()
        Runtime.configure(Main)
        Runtime.pidfile(Main.name)
        Runtime.scan(Main)
        Runtime.init(Main)
        Runtime.forever()

    @staticmethod
    def cmd(text):
        cli = Line()
        for txt in text.split(" ! "):
            evt = Event()
            evt.kind = "command"
            evt.orig = repr(cli)
            evt.text = txt
            Commands.command(evt)
            evt.wait()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Runtime.configure(Main)
        if Main.verbose:
            Runtime.banner()
        Runtime.scan(Main)
        Runtime.init(Main)
        csl = CSL()
        csl.start()
        Runtime.forever()

    @staticmethod
    def control():
        "cli script."
        if not Arguments.txt:
            return
        Main.all = True
        Runtime.configure(Main)
        Runtime.scan(Main)
        Scripts.cmd(Arguments.txt)

    @staticmethod
    def service():
        "service script."
        Runtime.privileges()
        Runtime.configure(Main)
        Runtime.scan(Main)
        Runtime.banner()
        Runtime.pidfile(Main.name)
        Runtime.init(Main)
        Runtime.forever()


def main():
    "main"
    Arguments.getargs()
    Main.ignore = "mbx,rst,udp,web,wsd"
    if Main.daemon:
        Runtime.wrap(Scripts.background)
    elif Main.console:
        Runtime.wrap(Scripts.console)
    elif Main.service:
        Runtime.wrap(Scripts.service)
    else:
        Runtime.wrap(Scripts.control)
