# This file is placed in the Public Domain.


"main"


import sys


from .defines import Boot, Client, Main, Message, Mods, Parse


class CLI(Client):

    def raw(self, text):
        "output to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


def main():
    "cli."
    Parse.parse(Main, " ".join(sys.argv[1:]))
    Main.user = True
    Boot.configure()
    Mods.scanner()
    cli = CLI()
    evt = Message()
    evt.orig = repr(cli)
    evt.text = Main.otxt
    Mods.command(evt)
