# This file is placed in the Public Domain.


"basic commands"


import time


from nixt.defines import Boot, Commands, Main, Mods, Time


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Commands.names)))


def mod(event):
    "list available modules."
    mods = ".".join(Mods.list())
    if not mods:
        event.reply("no modules available")
        return
    event.reply(mods)


def upt(event):
    "show uptiome."
    event.reply(Time.elapsed(time.time()-Time.starttime))


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Boot.core()}")
