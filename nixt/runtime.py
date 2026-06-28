# This file is placed in the Public Domain.


"main"


import sys


from .defines import Boot, Client, Main, Message, Mods, Parse
from .defines import Utils


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
