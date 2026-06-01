# This file is placed in the Public Domain.


from nixt.package import Mods


def mod(event):
    "list available modules."
    mods = ",".join(Mods.list())
    if not mods:
        event.reply("no modules available")
        return
    event.reply(mods)
