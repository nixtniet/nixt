# This file is placed in the Public Domain.


"main"


import argparse
import os
import readline
import sys
import time


from .defines import Boot, Client, Cmd, Engine, Main, Md5, Message
from .defines import Method, Mods, Utils


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
        group = theparser.add_mutually_exclusive_group()
        group.add_argument("--console", action="store_true", help="run as console.")
        group.add_argument("--daemon", action="store_true", help="run as background daemon.")
        group.add_argument("--service", action="store_true", help="run as service.")
        parser = theparser.add_argument_group()
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start.')
        optparser = theparser.add_argument_group()
        optionparser = theparser.add_argument_group()
        optionparser.add_argument("-l", "--level", default=Main.level, help='set loglevel.', metavar="level")
        optionparser.add_argument("-m", "--mods", default="", help='modules to load.', metavar="m1,m2")
        optionparser.add_argument("-p", "--path", default="", help='path to working directory.', metavar="path")
        optparser.add_argument("--admin", action="store_true", help="enable admin mode.")
        optparser.add_argument("--check", action="store_false", help=argparse.SUPPRESS)
        optparser.add_argument("--default", default="irc,rss", help=argparse.SUPPRESS)
        optparser.add_argument("--nochdir", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("--read", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("-u", "--user", action="store_true", help="use local mods directory.")
        args, arguments = theparser.parse_known_args()
        Main.otxt = " ".join(arguments)
        Method.update(Main.sets, args)


class Kernel(Boot):

    @classmethod
    def banner(cls):
        "hello."
        tmr = time.ctime(time.time()).replace("  ", " ")
        txt = "%s since %s %s (%s)" % (
            Main.name.upper(),
            tmr,
            Main.sets.level.upper() or "WARNING",
            Md5.core()
        )
        print(txt.replace("  ", " "))
        sys.stdout.flush()

    @classmethod
    def boot(cls, banner=True):
        cls.configure()
        if banner:
            cls.banner()
        cls.table()
        Mods.add(Cmd.cmd)

    @classmethod
    def daemon(cls):
        "run in the background."
        pid = os.fork()
        if pid != 0:
            os._exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 != 0:
            os._exit(0)
        if Main.sets.verhose:
            cls.null(sys.stdin)
            cls.null(sys.stdout)
            cls.null(sys.stderr)
        os.umask(0)
        if Main.sets.nochdir:
            os.chdir("/")
        os.nice(10)

    @classmethod
    def wrap(cls, func, *args, dofinal=None):
        "restore console."
        import termios
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            old = False
        cls.wrapped(func, *args)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
        if dofinal:
            dofinal()


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", Mods.command)

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
    def background():
        "background script."
        Main.sets.default = "irc,rss"
        Kernel.daemon()
        Kernel.privileges()
        Kernel.pid()
        Kernel.boot(False)
        Kernel.init()
        Kernel.forever()

    @staticmethod
    def console():
        "console script."
        readline.redisplay()
        Kernel.boot()
        if Main.sets.all:
            Main.sets.mods = ",".join(Mods.list())
        Kernel.init(True)
        csl = Console()
        csl.start()
        Kernel.forever()

    @staticmethod
    def control():
        "cli script."
        Kernel.boot(False)
        cli = CLI()
        cli.silent = False
        evt = Message()
        evt.orig = repr(cli)
        evt.text = Main.otxt
        if Main.sets.admin:
            mod = Mods.get("adm")
            Mods.scan(mod)
        Kernel.command(evt)

    @staticmethod
    def service():
        "service script."
        Main.sets.default = "irc,mdl,rss,wsd"
        Kernel.boot()
        Kernel.privileges()
        Kernel.pid()
        Kernel.init()
        Kernel.forever()


def main():
    Arguments.getargs()
    if Main.sets.service:
        Kernel.wrap(Scripts.service)
    elif Main.sets.console:
        Kernel.wrap(Scripts.console)
    elif Main.sets.daemon:
        Kernel.wrap(Scripts.background)
    else:
        Kernel.wrap(Scripts.control)
