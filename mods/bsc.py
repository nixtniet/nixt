#  This file is placed in the Public Domain.


"administrator"


import time


from nixt.command import Commands
from nixt.configs import Main
from nixt.package import Mods
from nixt.utility import Time, Utils


STARTTIME = time.time()


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Commands.commands(event.orig))))


def mod(event):
    "list available modules."
    mods = Mods.list()
    if not mods:
        event.reply("no modules available")
        return
    event.reply(mods)


def upt(event):
    "show uptiome."
    event.reply(Time.elapsed(time.time()-STARTTIME))


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Utils.md5sum(Mods.path('tbl') or '')[:7]}")
