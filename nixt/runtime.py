#!/usr/bin/env python3


"main"


import os
import readline
import sys


from .defines import Boot, Client, Cmd, Commands, Main, Message
from .defines import Mods, Parse, Workdir


class CLI(Client):

    def raw(self, text):
        "output to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


def main():
    "cli script."
    Parse.parse(Main, " ".join(sys.argv[1:]))
    Boot.configure()
    Mods.scanner()
    Commands.add(Cmd.cmd, Cmd.ver)
    cli = CLI()
    evt = Message()
    evt.orig = repr(cli)
    evt.text = Main.otxt
    Commands.command(evt)
