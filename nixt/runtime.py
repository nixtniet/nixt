# This file is placed in the Public Domain.


"main"


import os
import sys


from .caching import Workdir
from .command import Commands, Event, Main, Mods
from .handler import Client
from .objects import Methods


from . import modules as MODS


TXT = " ".join(sys.argv[1:])


class Line(Client):

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class Run:

    @staticmethod
    def boot():
        Main.wdr = os.path.expanduser(f"~/.{Main.name}")
        Methods.parse(Main, TXT)
        Methods.merge(Main, Main.sets)
        Workdir.skel()
        if Run.check("u"):
            Mods.add("mods")
        Mods.add(os.path.join(Main.wdr, "mods"), "modules")
        Mods.pkg(MODS)
        Commands.scanner()

    @staticmethod
    def check(opts):
        for word in TXT.split():
            if not word.startswith("-"):
                continue
            for char in opts:
                if char in word:
                    return True
        return False


def main():
    Run.boot()
    csl = Line()
    for txt in TXT.split(" ! "):
        evt = Event()
        evt.client = csl
        evt.text = txt
        Commands.command(evt)


if __name__ == "__main__":
    main()
