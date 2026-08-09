# This file is placed in the Public Domain.


"main"


import sys


from nixt.defines import Client, Cmd, Main, Message, Mods, Parse, Workdir


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
    Parse.parse(Main, " ".join(sys.argv[1:]))
    Mods.configure(Main.name, "--admin" in sys.argv)
    cli = CLI()
    cli.silent = False
    evt = Message()
    evt.orig = repr(cli)
    evt.text = Main.otxt
    Mods.command(evt)


if __name__ == "__main__":
    main()
