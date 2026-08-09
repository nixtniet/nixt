# This file is placed in the Public Domain.


"main"


import sys


from nixt.defines import Boot, Client, Main, Message, Mods, Parse


TXT = " ".join(sys.argv[1:])


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", Mods.command)

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()


def main():
    "cli script."
    Boot.boot("nixt", TXT)
    if "--admin" in sys.argv:
        mod = Mods.get("adm")
        Mods.scan(mod)
    cli = CLI()
    evt = Message()
    evt.orig = repr(cli)
    evt.text = Main.otxt
    Mods.command(evt)


if __name__ == "__main__":
    main()
