# This file is placed in the Public Domain.


"main"


import argparse
import sys


from nixt.defines import Boot, Client, Commands, Data, Main, Message
from nixt.defines import Method, Mods, Parse


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
        )
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
        optparser.add_argument("--wdr", default="", help="set modules directory.")
        optparser.add_argument("--nochdir", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("--admin", action="store_true", help="enable admin mode.")
        args, arguments = theparser.parse_known_args()
        Main.sets = Data()
        Method.update(Main.sets, args)
        Main.otxt = " ".join(arguments)


class Kernel(Boot):

    @classmethod
    def admin(self):
        if "--admin" in sys.argv:
            mod = Mods.get("adm")
            Commands.scan(mod)
        if "--scanner" in sys.argv:
            Mods.scanner()

    @classmethod
    def boot(cls):
        Parse.parse(Main, " ".join(sys.argv[1:]))
        Boot.configure()
        cls.admin()


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", Commands.command)

    def cmd(self, txt):
        evt = Message()
        evt.orig = repr(self)
        evt.text = txt
        Commands.command(evt)

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()


def main():
    "cli script."
    Arguments.getargs()
    Kernel.boot()
    cli = CLI()
    cli.cmd(" ".join(sys.argv[1:]))
