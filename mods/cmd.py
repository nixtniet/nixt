# This file is placed in the Public Domain.


"list available commands"


from nixt.defines import Commands


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Commands.cmds)))
