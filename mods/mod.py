# This file is placed in the Public Domain.


from nixt.package import Mods


def mod(event):
    event.reply(Mods.list())
