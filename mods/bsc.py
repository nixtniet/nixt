# This file is placed in the Public Domain.


"basic commands"


import time


from nixt.defines import Commands, Main, Time


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Commands.names)))


def mod(event):
    "list available modules."
    mods = list(Commands.names.keys())
    if not mods:
        event.reply("no modules available")
        return
    event.reply(" ".join(mods))


def upt(event):
    "show uptiome."
    event.reply(Time.elapsed(time.time()-Time.starttime))


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()}")
