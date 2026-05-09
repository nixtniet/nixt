# This file is placed in the Public Domain.


"main program"


import argparse
import logging
import sys
import time


from .defines import Boot, Commands, Console, Message, Main
from .defines import Object, Parse, Poller, Utils


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
        optparser.add_argument("--check", action="store_false", help="don't check core's md5sums")
        optparser.add_argument("--read", action="store_true", help="read config on boot.")
        optparser.add_argument("--default", default="irc,rss", help="set default modules.")
        optparser.add_argument("--nochdir", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("--wdr", default="", help='set working directory.', metavar="wdr")
        args, arguments = theparser.parse_known_args()
        Main.otxt = txt = " ".join(arguments)
        Object.update(Main, args)
        Parse.parse(Main, txt)


class Line(Console):

    @staticmethod
    def cmd(text):
        "do a command."
        cli = Line()
        for txt in text.split(" ! "):
            evt = Message()
            evt.kind = "command"
            evt.orig = repr(cli)
            evt.text = txt
            Commands.command(evt)
            evt.wait()

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class CSL(Line):

    '''
    def poll(self):
        "poll for an event."
        evt = Message()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        return evt
    '''
    pass

class Runs:

    @staticmethod
    def banner(cfg):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        txt = "%s %s since %s %s (%s)" % (
            cfg.name.upper(),
            cfg.version,
            tme,
            cfg.level.upper() or "INFO",
            Boot.md5()
        )
        print(txt.replace("  ", " "))
        sys.stdout.flush()

    @staticmethod
    def boot(cfg):
        Boot.configure(cfg)
        if cfg.verbose:
            Runs.banner(cfg)
        if cfg.check and cfg.verbose and Boot.core():
            logging.info("core ok")
        

class Scripts:

    @staticmethod
    def background():
        "background script."
        Boot.daemon(Main.verbose, Main.nochdir)
        Boot.privileges()
        Boot.boot(Main)
        Boot.pidfile(Main.name)
        Boot.init(Main.mods or Main.default)
        Boot.forever()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Runs.boot(Main)
        Boot.init(Main.mods, Main.wait)
        csl = CSL()
        csl.start()
        Boot.forever()

    @staticmethod
    def control():
        "cli script."
        Runs.boot(Main)
        Main.check = False
        Line.cmd(Main.otxt)

    @staticmethod
    def service():
        "service script."
        Boot.privileges()
        Runs.boot(Main)
        Boot.pidfile(Main.name)
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
