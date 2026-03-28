# This file is placed in the Public Domain.


"configuration"


from nixt.configs import Main
from nixt.objects import Data, Methods, Object
from nixt.package import Mods
from nixt.persist import Disk, Locate


def krn(event):
    if not event.sets:
        event.reply(Methods.fmt(Main, skip="gets,sets,silent"))
        return
    print(event)
    Methods.edit(Main, event.sets)
    Disk.write(Main, "kernel", "config")
    event.reply("ok")
