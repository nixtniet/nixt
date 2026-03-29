# This file is placed in the Public Domain.


"configuration"


from nixt.configs import Main
from nixt.objects import Data, Methods
from nixt.persist import Disk


def krn(event):
    cfg = Data()
    Disk.read(cfg, "kernel", "config")
    if not event.sets:
        event.reply(Methods.fmt(cfg, skip="gets,sets,silent"))
        return
    Methods.edit(cfg, event.sets)
    Disk.write(cfg, "kernel", "config")
    event.reply("ok")
