#  This file is placed in the Public Domain.


"administrator"


from nixt.caching import Workdir
from nixt.command import Commands, Main, Mods
from nixt.objects import Json


def configure():
    tbl.skip = "irc"
    wdr.skip = "irc"


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


def tbl(event):
    "create table."
    Mods.md5s = {}
    for name, module in Mods.all(True):
        Commands.scan(module)
    event.reply("# This file is placed in the Pubic Domain.\n\n")
    event.reply('"tables"\n\n')
    event.reply(f"NAMES = {Json.dumps(Commands.names, indent=4)}\n\n")
    event.reply(f"MD5 = {Json.dumps(Mods.md5s, indent=4)}")


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Main.version}")


def wdr(event):
    "show working directory."
    event.reply(Workdir.workdir())
