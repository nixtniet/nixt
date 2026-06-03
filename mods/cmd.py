# This file is placed in the Public Domain.


"list commands"


from nixt.defines import Mods


whitelist = ['show']


def show(event):
    "list available commands."
    event.reply(",".join(sorted(Mods.list())))
