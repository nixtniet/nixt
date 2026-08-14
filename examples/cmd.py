# This file is placed in the Public Domain.


"list commands"


from nixt.package import Commands, Mods


def cmd(event):
    "show commands."
    event.reply(",".join(sorted(Mods.names or Commands.cmds)))
