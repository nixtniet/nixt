# This file is placed in the Public Domain.


"main"


import argparse
import readline
import sys


from .defines import Client, Cmd, Commands, Engine, Kernel, Main, Message
from .defines import Mods, Method, Utils


class Arguments:

    @classmethod
    def getargs(cls):
        "parse commandline arguments."
        Main.name = Main.name or Utils.pkgname(Main)
        theparser = argparse.ArgumentParser(
            prog=Main.name,
            description=f'{Main.name.upper()}',
            epilog='use "%(prog)s cmd" for a list of commands.',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage='''%(prog)s    [-h|-s] [-a] [-v] [-w] [-l level] [-m m1,m2] [-p path]\n       %(prog)sctl [cmd] [key=val] [key==val]\n       %(prog)sd'''
        )
        group = theparser.add_mutually_exclusive_group()
        group.add_argument("-s", "--service", action="store_true", help="run as service.")
        parser = theparser.add_argument_group()
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start.')
        optionparser = theparser.add_argument_group()
        optionparser.add_argument("-l", "--level", default="warning", help='set loglevel.', metavar="level")
        optionparser.add_argument("-m", "--mods", default="", help='modules to load.', metavar="m1,m2")
        optionparser.add_argument("-p", "--path", default="", help='path to working directory.', metavar="path")
        optparser = theparser.add_argument_group()
        optparser.add_argument("--default", default="irc,mdl,rss,wsd", help=argparse.SUPPRESS)
        optparser.add_argument("--moddir", default=Utils.moddir(), help="set modules directory.")
        optparser.add_argument("--nochdir", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("--admin", action="store_true", help="enable admin mode.")
        args, arguments = theparser.parse_known_args()
        Main.otxt = " ".join(arguments)
        Method.update(Main.sets, args)


class CLI(Client, Engine):

    def __init__(self):
        Client.__init__(self)
        Engine.__init__(self)
        self.register("command", Commands.command)

    def after(self, event):
        "wait for event to finish"
        event.wait()

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()


class Console(CLI):

    def __init__(self):
        CLI.__init__(self)
        self.silent = True

    def poll(self):
        "return event."
        evt = Message()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        self.put(evt)
        return evt


class Scripts:

    @staticmethod
    def banner():
        print(Kernel.banner())
        sys.stdout.flush()

    @staticmethod
    def background():
        "background script."
        Main.sets.default = "irc,rss"
        Kernel.daemon()
        Commands.add(Cmd.cmd)
        Kernel.configure()
        Kernel.privileges()
        Kernel.pid()
        Kernel.init()
        Kernel.forever()

    @staticmethod
    def console():
        "console script."
        readline.redisplay()
        Arguments.getargs()
        Commands.add(Cmd.cmd)
        Kernel.configure()
        Scripts.banner()
        if Main.sets.all:
            Main.sets.mods = ",".join(Mods.list())
        Kernel.init(True)
        csl = Console()
        csl.start()
        Kernel.forever()

    @staticmethod
    def control():
        "cli script."
        Arguments.getargs()
        Commands.add(Cmd.cmd, Cmd.srv, Cmd.tbl)
        Kernel.configure()
        cli = CLI()
        cli.silent = False
        evt = Message()
        evt.orig = repr(cli)
        evt.text = Main.otxt
        Commands.command(evt)

    @staticmethod
    def service():
        "service script."
        Arguments.getargs()
        Commands.add(Cmd.cmd)
        Kernel.configure()
        Kernel.privileges()
        Kernel.pid()
        Scripts.banner()
        Kernel.init()
        Kernel.forever()


def main():
    if "-s" in sys.argv:
        Kernel.wrap(Scripts.service)
    else:
        Kernel.wrap(Scripts.console)
