# This file is placed in the Public Domain.


"main"


import os
import readline
import sys
import time


from .defines import Boot, Client, Cmd, Engine, Main, Md5, Message, Mods


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
        if "v" not in Main.opts:
            cls.null(sys.stdin)
            cls.null(sys.stdout)
            cls.null(sys.stderr)
        os.umask(0)
        if "n" in Main.opts:
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


class CLI(Engine, Client):

    def __init__(self):
        Engine.__init__(self)
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
        Kernel.parse(Main, " ".join(sys.argv[1:]))
        Kernel.boot()
        if "all" in Main.opts:
            Main.sets.mods = ",".join(Mods.list())
        Kernel.init(True)
        csl = Console()
        csl.start()
        Kernel.forever()

    @staticmethod
    def control():
        "cli script."
        Kernel.parse(Main, " ".join(sys.argv[1:]))
        Kernel.boot(False)
        cli = CLI()
        cli.silent = False
        evt = Message()
        evt.orig = repr(cli)
        evt.text = Main.otxt
        if "admin" in Main.opts:
            mod = Mods.get("adm")
            Mods.scan(mod)
        Kernel.command(evt)

    @staticmethod
    def service():
        "service script."
        Kernel.parse(Main, " ".join(sys.argv[1:]))
        Main.sets.default = "irc,mdl,rss,wsd"
        Kernel.boot()
        Kernel.privileges()
        Kernel.pid()
        Kernel.init()
        Kernel.forever()


def main():
    if "-s" in sys.argv or "--service" in sys.argv:
        Kernel.wrap(Scripts.service)
    elif "--console" in sys.argv:
        Kernel.wrap(Scripts.console)
    elif "--daemon" in sys.argv:
        Kernel.wrap(Scripts.background)
    else:
        Kernel.wrap(Scripts.control)
