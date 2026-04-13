# This file is placed in the Pubic Domain.


"tables"


from nixt.booting import Boot
from nixt.command import Commands
from nixt.encoder import Json
from nixt.package import Mods
from nixt.persist import Disk


def tbl(event):
    "create table."
    Mods.md5s = {}
    for name, module in Mods.all(True):
        Commands.scan(module)
    Disk.write(Boot.md5s, "core", "tables")
    Disk.write(Commands.names, "names", "tables")
    Disk.write(Mods.md5s, "modules", "tables")
    event.ok()


tbl.skip = "irc,csl"
