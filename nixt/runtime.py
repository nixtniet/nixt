# This file is placed in the Public Domain.


"main"


import logging
import os
import sys
import time


from .command import Commands, Event, Main, Mods
from .handler import Client
from .objects import Data, Methods, Object
from .utility import Utils


from . import modules as MODS


TXT = " ".join(sys.argv[1:])


class Line(Client):

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class Run:

    @classmethod
    def banner(cls):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        print("%s %s since %s %s (%s)" % (
            Main.name.upper(),
            Main.version,
            tme,
            Main.level.upper() or "INFO",
            Utils.md5sum(Mods.path("tbl") or "")[:7]
        ))
        sys.stdout.flush()
        return Main.version

    @staticmethod
    def check(opts):
        for word in TXT.split():
            if not word.startswith("-"):
                continue
            for char in opts:
                if char in word:
                    return True
        return False

    @staticmethod
    def cmd(text):
        "parse text for command and run it."
        cli = Line()
        for txt in TXT.split(" ! "):
            evt = Event()
            evt.client = cli
            evt.orig = repr(cli)
            evt.text = txt
            Commands.command(evt)
        return evt

    @classmethod
    def wrap(cls, func, *args):
        "restore console."
        import termios
        old = None
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            pass
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as ex:
            logging.exception(ex)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def main():
    Main.wdr = os.path.expanduser(f"~/.{Main.name}")
    Mods.add("mods")
    Mods.pkg(MODS)
    Methods.parse(Main, TXT)
    Commands.scanner()
    Run.cmd(TXT)


if __name__ == "__main__":
    Run.wrap(main)
