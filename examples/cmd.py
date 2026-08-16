# This file is placed in the Public Domain.


"list commands"


from nixt.defines import Commands


def cmd(event):
    "show commands."
    event.reply(",".join(sorted(Commands.names or Commands.cmds)))
