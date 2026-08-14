# This file is placed in the Public Domain.


"administrator"


import inspect
import os


from nixt.configs import Main
from nixt.encoder import Json
from nixt.package import Commands, Mods
from nixt.utility import Md5


def tbl(event):
    "create table."
    if not Main.sets.admin:
        event.reply("creating tables needs --admin")
        return
    core = {}
    md5s = {}
    Mods.names = {}
    for name in Mods.list():
        module = Mods.get(name)
        md5s[name] = Md5.md5(module.__file__)
        for cmd in Commands.scan(module):
            Mods.names[cmd.__name__] = cmd.__module__.split(".")[-1]
    corepath = os.path.dirname(inspect.getsourcefile(Mods))
    Md5.createmd5(corepath, core)
    event.reply("# This file is placed in the Public Domain.")
    event.reply("\n")
    event.reply('"static tables"')
    event.reply("\n")
    event.reply(f"CORE = {Json.dumps(core, indent=4, sort_keys=True)}")
    event.reply("\n")
    event.reply(f"MODULES = {Json.dumps(md5s, indent=4, sort_keys=True)}")
    event.reply("\n")
    event.reply(f"NAMES = {Json.dumps(Mods.names, indent=4, sort_keys=True)}")
