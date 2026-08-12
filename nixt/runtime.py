# This file is placed in the Public Domain.


"main"


import argparse
import sys


from nixt.defines import Boot, Client, Cmd, Commands, Data, Main, Message
from nixt.defines import Method


class Arguments:

    @classmethod
    def getargs(cls):
        "parse commandline arguments."
        Main.name = Main.name or Method.pkgname(Main)
        theparser = argparse.ArgumentParser(
            prog=Main.name,
            description=f'{Main.name.upper()}',
            epilog='use "%(prog)s cmd" for a list of commands.',
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        optionparser = theparser.add_argument_group()
        optionparser.add_argument("-l", "--level", default="warning", help='set loglevel.', metavar="level")
        optionparser.add_argument("-m", "--mods", default="", help='modules to load.', metavar="m1,m2")
        optionparser.add_argument("-p", "--path", default="", help='path to working directory.', metavar="path")
        optionparser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        optparser = theparser.add_argument_group()
        optparser.add_argument("--admin", action='store_true', help="enable admin mode.")
        optparser.add_argument("--scanner", action="store_true", help="do full modules scan on boot.")
        optparser.add_argument("--wdr", default="", help="set modules directory.")
        args, arguments = theparser.parse_known_args()
        Main.sets = Data()
        Method.update(Main.sets, args)
        Main.otxt = " ".join(arguments)
        Commands.add(Cmd.cmd)


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
    Boot.configure()
    cli = CLI()
    cli.cmd(" ".join(sys.argv[1:]))
