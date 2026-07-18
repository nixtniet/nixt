# #!/usr/bin/env python3
# This file is placed in the Public Domain.


"program your own commands"


import sys


# sys.path.insert(0, os.getcwd())


from nixt.defines import Client, Cmd, Commands, Message, Mods


class CLI(Client):

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))
        sys.stdout.flush()


def main():
    "cli script."
    # Parse.parse(Main, " ".join(sys.argv[1:]))
    Commands.add(Cmd.srv, Cmd.tbl)
    Mods.configure()
    cli = CLI()
    evt = Message()
    evt.orig = repr(cli)
    evt.text = " ".join(sys.argv[1:])
    Commands.command(evt)


if __name__ == "__main__":
    main()
