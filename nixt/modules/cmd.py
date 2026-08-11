# This file is placed in the Public Domain.


"list available commands"


from nixt.defines import Mods


def cmd(event):
    "show commands."
    event.reply(",".join(Mods.listcmds()))
