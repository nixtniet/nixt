# This file is placed in the Public Domain.


"main"


import sys


from nixt.defines import Boot, Client, Commands, Main, Message
from nixt.defines import Mods, Parse


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
    Kernel.boot()
    cli = CLI()
    cli.cmd(" ".join(sys.argv[1:]))
