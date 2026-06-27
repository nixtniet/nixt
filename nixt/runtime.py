#!/usr/bin/env python3
# This file is placed in the Public Domain.


"main"


import os
import readline
import sys
import time


sys.path.insert(0, os.getcwd())


from nixt.defines import Boot, Client, Main, Message, Mods, Object, Parse
from nixt.defines import Utils, Workdir


class CLI(Client):

    def raw(self, text):
        print(text.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()


def main():
    Parse.parse(Main, " ".join(sys.argv[1:]))
    Boot.configure()
    Mods.scanner()
    cli = CLI()
    evt = Message()
    evt.orig = repr(cli)
    evt.text = Main.otxt
    Mods.command(evt)


if __name__ == "__main__":
    Utils.wrapped(main)
