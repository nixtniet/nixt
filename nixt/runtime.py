# This file is placed in the Public Domain.


"main"


import sys


from nixt.defines import Boot, Client, Cmd, Commands, Message, Mods


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", Commands.command)

    def admin(self):
        if "--admin" in sys.argv:
            mod = Mods.get("adm")
            Commands.scan(mod)

    def cmd(self, txt):
        evt = Message()
        evt.orig = repr(self)
        evt.text = txt
        Commands.command(evt)

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()


def main():
    "cli script."
    Boot.configure("nixt", "warning")
    Commands.add(Cmd.cmd)
    cli = CLI()
    cli.admin()
    cli.cmd(" ".join(sys.argv[1:]))
