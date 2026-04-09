#  This file is placed in the Public Domain.


"administrator"


from nixt.caching import Workdir
from nixt.command import Commands, Main, Mods


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Commands.commands(event.orig))))


def mod(event):
    "list available modules."
    mods = Mods.list(Main.ignore)
    if not mods:
        event.reply("no modules available")
        return
    event.reply(mods)


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Main.version}")


def wdr(event):
    "show working directory."
    event.reply(Workdir.workdir())
