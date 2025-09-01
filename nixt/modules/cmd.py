# This file is placed in the Public Domain.


"list commands"


from ..cmds import Commands


def cmd(event):
    event.reply(",".join(sorted(Commands.names)))
