# This file is placed in the Public Domain.


"main"


import os
import readline
import sys
import time


from ..library import Client
from ..persist import Workdir


from .booting import Boot
from .configs import Main
from .message import Message
from .package import Cmd, Md5, Mods
from .parsers import Parse


class Kernel(Boot):

    pid = Workdir.pid

    @classmethod
    def admin(cls):
        if Kernel.check("admin"):
            mod = Mods.get("adm")
            Mods.scan(mod)
            cls.cmd(Main.otxt)
            return True
        return False

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
        "starting."
        Workdir.configure(Main.name)
        Mods.configure(Main.name)
        cls.configure()
        Mods.add(Cmd.cmd)
        if banner:
            cls.banner()

    @classmethod
    def cmd(cls, txt):
        cli = CLI()
        cli.silent = False
        evt = Message()
        evt.orig = repr(cli)
        evt.text = txt
        Mods.command(evt)

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
    def help(cls):
        if Kernel.check("h,help"):
            mod = Mods.get("hlp")
            Mods.scan(mod)
            cls.cmd("hlp")
            return True
        return False

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
        "wait for event to finish."
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


class Scripts:

    @staticmethod
    def background():
        "background script."
        Main.sets.default = "irc,rss"
        Kernel.daemon()
        Kernel.privileges()
        Kernel.pid(Main.name)
        Kernel.boot(False)
        Kernel.init()
        Kernel.forever()

    @staticmethod
    def console():
        "console script."
        readline.redisplay()
        Kernel.boot()
        Kernel.init(True)
        csl = Console()
        csl.start()
        Kernel.forever()

    @staticmethod
    def control():
        "cli script."
        Kernel.boot(False)
        if Kernel.help():
            return
        if Kernel.admin():
            return
        Kernel.cmd(Main.otxt)

    @staticmethod
    def service():
        "service script."
        Main.sets.default = "irc,mdl,rss,wsd"
        Kernel.boot()
        Kernel.privileges()
        Kernel.pid(Main.name)
        Kernel.init()
        Kernel.forever()


def main():
    Parse.parse(Main, " ".join(sys.argv[1:]))
    if Kernel.check("service"):
        Kernel.wrap(Scripts.service)
    elif Kernel.check("console"):
        Kernel.wrap(Scripts.console)
    elif Kernel.check("daemon"):
        Kernel.wrap(Scripts.background)
    else:
        Kernel.wrap(Scripts.control)
