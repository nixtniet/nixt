# This file is placed in the Public Domain.


"control"


from nixt.defines import Mods
from nixt.defines import Commands, Console, Event,  Main, Methods, Runtime


class Line(Console):

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


def cmd(text):
    cli = Line()
    for txt in text.split(" ! "):
        evt = Event()
        evt.kind = "command"
        evt.orig = repr(cli)
        evt.text = txt
        Commands.command(evt)
        evt.wait()


def main():
    "cli script."
    import sys
    txt = " ".join(sys.argv[1:])
    if not txt:
        return
    Main.user = True
    Methods.parse(Main, txt)
    Runtime.configure(Main)
    Main.mods = Mods.list()
    Runtime.scanner(Main)
    cmd(txt)
