#!/usr/bin/env python3
# This file is placed in the Public Domain.


"main"


import os
import readline
import sys
import time


sys.path.insert(0, os.getcwd())


from nixt.defines import Client, Cmd, Main, Message, Md5, Mods, Parse, Workdir


class Kernel:

    @classmethod
    def admin(cls):
        if "--admin" in sys.argv:
            mod = Mods.get("adm")
            Mods.scan(mod)
            cls.cmd(Main.otxt)
            return True
        return False

    @classmethod
    def cmd(cls, txt):
        cli = CLI()
        cli.silent = False
        evt = Message()
        evt.orig = repr(cli)
        evt.text = txt
        Mods.command(evt)

    @classmethod
    def configure(cls, name):
        Parse.parse(Main, " ".join(sys.argv[1:]))
        Workdir.configure(name)
        Mods.configure(name)
        Mods.add(Cmd.cmd)


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


def main():
    "cli script."
    Kernel.configure("nixt")
    if Kernel.admin():
         return
    Kernel.cmd(Main.otxt)


if __name__ == "__main__":
    main()
