# This file is placed in the Public Domain.


"list commands"


from nixt.defines import Mods


def show(event):
    "list available commands."
    event.reply(",".join(sorted(Mods.list())))
