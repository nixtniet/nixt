# This file is placed in the Public Domain.


"commands"


from nixt.package import Commands


def cmd(event):
    "show commands."
    event.reply(",".join(sorted(Commands.cmds)))
