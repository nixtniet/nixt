# This file is placed in the Public Domain.


"administrator"


from nixt.command import Commands
from nixt.defines import Main
from nixt.encoder import Json
from nixt.package import Mods


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Commands.names.keys() or Commands.cmds.keys())))


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
