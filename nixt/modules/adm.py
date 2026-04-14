#  This file is placed in the Public Domain.


"administrator"


from nixt.command import Commands
from nixt.configs import Main
from nixt.package import Mods
from nixt.utility import Utils


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
    event.reply(f"{Main.name.upper()} {Utils.md5sum(Mods.path('tbl'))[:7]}")
