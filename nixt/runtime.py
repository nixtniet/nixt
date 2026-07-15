# This file is placed in the Public Domain.


"program your own commands"


import sys


from .defines import Boot, Client, Cmd, Commands, Main, Message


class CLI(Client):

    def raw(self, text):
        "output to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class Wrap:

    @staticmethod
    def wrap(func, *args):
        "restore console."
        import termios
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            old = False
        Boot.wrapped(func, *args)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)

    @staticmethod
    def wrapped():
        "wrap main."
        Wrap.wrap(main)


def main():
    "cli script."
    Boot.parse(Main, " ".join(sys.argv[1:]))
    Boot.configure()
    Boot.scanner()
    Commands.add(Cmd.cmd)
    cli = CLI()
    cli.silent = False
    evt = Message()
    evt.orig = repr(cli)
    evt.text = Main.otxt
    Boot.command(evt)


if __name__ == "__main__":
    Wrap.wrapped()
