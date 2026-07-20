# This file is placed in the Public Domain.


"main"


import argparse
import readline
import sys


from .defines import Boot, Client, Cmd, Engine, Main, Message
from .defines import Mods, Method, Parse, Utils


class CLI(Client, Engine):

    def __init__(self):
        Client.__init__(self)
        Engine.__init__(self)
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


class Kernel(Boot):

    @classmethod
    def banner(cls):
        print(Boot.banner())
        sys.stdout.flush()


class Scripts:

    @staticmethod
    def background():
        "background script."
        Main.sets.default = "irc,rss"
        Kernel.daemon()
        Kernel.add(Cmd.cmd)
        Kernel.configure()
        Kernel.privileges()
        Kernel.pid()
        Kernel.init()
        Kernel.forever()

    @staticmethod
    def console():
        "console script."
        readline.redisplay()
        Kernel.parse(Main, " ".join(sys.argv[1:]))
        Kernel.add(Cmd.cmd)
        Kernel.configure()
        Kernel.banner()
        if "a" in Main.opts:
            Main.sets.mods = ",".join(Mods.list())
        Kernel.init(True)
        csl = Console()
        csl.start()
        Kernel.forever()

    @staticmethod
    def control():
        "cli script."
        Kernel.parse(Main, " ".join(sys.argv[1:]))
        Kernel.add(Cmd.cmd, Cmd.srv, Cmd.tbl)
        Kernel.configure()
        cli = CLI()
        cli.silent = False
        evt = Message()
        evt.orig = repr(cli)
        evt.text = Main.otxt
        Mods.command(evt)

    @staticmethod
    def service():
        "service script."
        Kernel.parse(Main, " ".join(sys.argv[1:]))
        Kernel.add(Cmd.cmd)
        Kernel.configure()
        Kernel.privileges()
        Kernel.pid()
        Kernel.banner()
        Kernel.init()
        Kernel.forever()


def main():
    if "-s" in sys.argv:
        Kernel.wrap(Scripts.service)
    else:
        Kernel.wrap(Scripts.console)
