#!/usr/bin/env python3
# This file is placed in the Public Domain.


"nixt"


import argparse


from .defines import Boot, Commands, Console, Event, Main, Object, Parse


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
                                         usage='''%(prog)s [-c|d|h|s] [-l level] [-m m1,m2] [-w wdr] [-a] [-r] [-v] [-u] [-x]\n       %(prog)s [cmd] [arg=val] [arg==val]'''
                                        )
        group = theparser.add_mutually_exclusive_group()
        group.add_argument("-c", "--console", action="store_true", help="run as console.")
        group.add_argument("-d", "--daemon", action="store_true", help="run as background daemon.")
        group.add_argument("-s", "--service", action="store_true", help="run as service.")
        parser = theparser.add_argument_group()
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-l", "--level", default=Main.level, help='set loglevel.', metavar="level")
        parser.add_argument("-m", "--mods", default="", help='modules to load.', metavar="m1,m2")
        parser.add_argument("-r", "--read", action="store_true", help="read config on start.")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wdr", default="", help='set working directory.', metavar="wdr")
        parser.add_argument("-u", "--user", action="store_true", help="use local mods directory.")
        parser.add_argument("-x", "--admin", action="store_true", help="enable admin mode.")
        parser.add_argument("--nochdir", action="store_true", help=argparse.SUPPRESS)
        parser.add_argument("--noignore", action="store_true", help=argparse.SUPPRESS)
        cls.args, arguments = theparser.parse_known_args()
        cls.txt = " ".join(arguments)
        Object.update(Main, cls.args)
        Parse.parse(Main, cls.txt)


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
        Main.read = True
        Main.init = Main.init or "irc,rss"
        Boot.daemon(Main.verbose, Main.nochdir)
        Boot.privileges()
        Boot.configure(Main)
        Boot.scanner(Main)
        Boot.init(Main)
        Boot.forever()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Boot.configure(Main)
        if Main.verbose:
            Boot.banner()
        Boot.scanner(Main)
        Boot.init(Main)
        csl = CSL()
        csl.start(daemon=True)
        Boot.forever()

    @staticmethod
    def control():
        "cli script."
        if not Arguments.txt:
            return
        Main.all = True
        Boot.configure(Main)
        Boot.scanner(Main)
        cmd(Arguments.txt)

    @staticmethod
    def service():
        "service script."
        Main.read = True
        Main.init = Main.init or "irc,rss"
        Boot.privileges()
        Boot.configure(Main)
        Boot.scanner(Main)
        Boot.banner()
        Boot.init(Main)
        Boot.forever()


def cmd(text):
    cli = Line()
    for txt in text.split(" ! "):
        evt = Event()
        evt.kind = "command"
        evt.orig = repr(cli)
        evt.text = txt
        Commands.command(evt)
        evt.wait()


def main():
    "main"
    Arguments.getargs()
    Main.ignore = "man,mbx,rst,tmr,udp,web"
    if not Main.admin:
        Main.ignore += ",adm"
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
