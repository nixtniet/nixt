# This file is placed in the Public Domain.


"main"


import argparse
import inspect
import logging
import os
import readline
import sys
import time
import _thread


from .defines import Boot, Client, Commands, Logging, Main, Message
from .defines import Mods, Md5, Object, Utils, Thread, Workdir, j


Main.name = Utils.pkgname(Commands)


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
            usage='''%(prog)s [-c|-d|-h|-s] [-a] [-v] [-w] [-l level] [-m m1,m2] [-p path]\n       %(prog)s [cmd] [key=val] [key==val]'''
        )
        group = theparser.add_mutually_exclusive_group()
        group.add_argument("-c", "--console", action="store_true", help="run as console.")
        group.add_argument("-d", "--daemon", action="store_true", help="run as background daemon.")
        group.add_argument("-s", "--service", action="store_true", help="run as service.")
        parser = theparser.add_argument_group()
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start.')
        optionparser = theparser.add_argument_group()
        optionparser.add_argument("-l", "--level", default=Main.level, help='set loglevel.', metavar="level")
        optionparser.add_argument("-m", "--mods", default="", help='modules to load.', metavar="m1,m2")
        optionparser.add_argument("-p", "--path", default="", help='path to working directory.', metavar="path")
        optparser = theparser.add_argument_group()
        optparser.add_argument("--admin", action="store_true", help="enable admin mode.")
        optparser.add_argument("--check", action="store_false", help=argparse.SUPPRESS)
        optparser.add_argument("--default", default="irc,rss", help=argparse.SUPPRESS)
        optparser.add_argument("--nochdir", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("--read", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("--user", action="store_false", help="use local mods directory.")
        args, arguments = theparser.parse_known_args()
        Main.otxt = " ".join(arguments)
        Object.update(Main, args)


class CLI(Client):

    def cmd(self, text):
        "do command."
        evt = Message()
        evt.orig = repr(self)
        evt.text = text
        Commands.command(evt)
        evt.wait()
        return evt

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()


class Console(CLI):

    def __init__(self):
        CLI.__init__(self)
        self.silent = True

    def handle(self, event):
        "handle event."
        Commands.command(event)

    def poll(self):
        "return event."
        evt = Message()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        return evt


class Runs(Boot):

    @classmethod
    def banner(cls):
        "hello"
        tme = time.ctime(time.time()).replace("  ", " ")
        txt = "%s %s since %s %s (%s)" % (
            Main.name.upper(),
            Main.version,
            tme,
            Main.level.upper() or "INFO",
            cls.core()
        )
        print(txt.replace("  ", " "))
        sys.stdout.flush()

    @classmethod
    def daemon(cls, verbose=False, nochdir=False):
        "run in the background."
        pid = os.fork()
        if pid != 0:
            os._exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 != 0:
            os._exit(0)
        if not verbose:
            with open('/dev/null', 'r', encoding="utf-8") as sis:
                os.dup2(sis.fileno(), sys.stdin.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as sos:
                os.dup2(sos.fileno(), sys.stdout.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as ses:
                os.dup2(ses.fileno(), sys.stderr.fileno())
        os.umask(0)
        if not nochdir:
            os.chdir("/")
        os.nice(10)

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(0.01)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @classmethod
    def wrap(cls, func, *args, final=None):
        "restore console."
        import termios
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            old = False
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            print("")
        except Exception as ex:
            logging.exception(ex)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
        if final:
            final()

    pid = Workdir.pid


class Scripts:

    @staticmethod
    def background():
        "background script."
        Runs.daemon(Main.verbose, Main.nochdir)
        Runs.privileges()
        Runs.pid(Main.name)
        Runs.scanner()
        Runs.init(Main.mods or Main.default)
        Runs.forever()

    @staticmethod
    def console():
        "console script."
        readline.redisplay()
        if Main.verbose:
            Runs.banner()
        if Main.all:
            Main.mods = ",".join(Mods.list())
        Runs.scanner()
        if not Runs.init(Main.mods, Main.wait):
            return
        csl = Console()
        csl.start()
        Runs.forever()

    @staticmethod
    def control():
        "cli script."
        Runs.scanner()
        cli = CLI()
        cli.silent = False
        cli.cmd(Main.otxt)

    @staticmethod
    def service():
        "service script."
        Runs.privileges()
        Runs.pid(Main.name)
        Runs.scanner()
        Runs.init(Main.mods or Main.default)
        Runs.forever()


def main():
    "main"
    Arguments.getargs()
    Runs.configure()
    if Main.daemon:
        Runs.wrap(Scripts.background)
    elif Main.console:
        Runs.wrap(Scripts.console)
    elif Main.service:
        Runs.wrap(Scripts.service)
    else:
        Runs.wrap(Scripts.control)


if __name__ == "__main__":
    main()
