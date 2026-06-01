# This file is placed in the Public Domain.


"list commands"


from nixt.package import Mods


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Mods.list())))
