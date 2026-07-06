# This file is placed in the Public Domain.


"main"


import sys


from .defines import Boot, Client, Commands, Main, Message, Md5, Mods, Parse


class CLI(Client):

    def raw(self, text):
        "output to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Commands.cmds)))


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Md5.core()}")


def main():
    "cli."
    Parse.parse(Main, " ".join(sys.argv[1:]))
    Boot.configure()
    Mods.scanner()
    Commands.add(cmd, ver)
    cli = CLI()
    evt = Message()
    evt.orig = repr(cli)
    evt.text = Main.otxt
    Commands.command(evt)
