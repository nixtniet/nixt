# This file is placed in the Public Domain.


"main"


import argparse
import sys


from .defines import Boot, Client, Cmd, Commands, Data, Main, Message
from .defines import Method, Mods, Workdir


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
        optionparser.add_argument("-n", "--name", default="nixt", help="name of the program.")
        optionparser.add_argument("-p", "--path", default="", help='path to modules directory.', metavar="path")
        optionparser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        optparser = theparser.add_argument_group()
        optparser.add_argument("--admin", action='store_true', help="enable admin mode.")
        optparser.add_argument("--scanner", action="store_true", help="do full modules scan on boot.")
        optparser.add_argument("--wdr", default="", help="set modules directory.")
        args, arguments = theparser.parse_known_args()
        Main.sets = Data()
        Method.update(Main.sets, args)
        Main.otxt = " ".join(arguments)


class Kernel(Boot):

    @classmethod
    def boot(cls):
        Arguments.getargs()
        cls.configure(Main)
        Mods.dir(Mods.moddir())
        Mods.dir(Workdir.moddir())
        Commands.add(Cmd.cmd)
        if Main.sets.all:
            Main.sets.mods = ",".join(Mods.list())
        if Main.sets.admin:
            Commands.add(Cmd.tbl)
        if Main.sets.scanner or Main.sets.all:
            Commands.scanner()
        else:
            Commands.table()
        Mods.table()


class CLI(Client):

    def __init__(self):
        Client.__init__(self)

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()


def main():
    "cli script."
    Kernel.boot()
    cli = CLI()
    evt = Message()
    evt.orig = repr(cli)
    evt.text = " ".join(sys.argv[1:])
    Commands.command(evt)
    evt.wait()


def __dir__():
    return (
        'Arguments',
        'Kernel',
        'CLI',
        'main'
    )
