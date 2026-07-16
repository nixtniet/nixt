# This file is placed in the Public Domain.


"program your own commands"


import sys


from .defines import Cmd, Commands, Main, Message, Mods


def raw(text):
    "output to console."
    print(text.encode('utf-8', 'replace').decode("utf-8"))


def main():
    "cli script."
    Commands.add(Cmd.cmd)
    Mods.configure()
    Mods.scanner()
    evt = Message()
    evt.text = " ".join(sys.argv[1:])
    Commands.command(evt)
    for text in evt.result:
        raw(text)


if __name__ == "__main__":
    main()
