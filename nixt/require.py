# This file is placed in the Public Domain.


"required commands"


import inspect
import os


from .command import Commands
from .encoder import Json
from .hashing import Md5
from .package import Mods


class Cmd:

    @staticmethod
    def cmd(event):
        "show commands."
        event.reply(",".join(sorted(Commands.names or Commands.cmds)))

    @staticmethod
    def tbl(event):
        "create table."
        core = {}
        md5s = {}
        Commands.names = {}
        for name in Mods.list():
            module = Mods.get(name)
            md5s[name] = Md5.md5(module.__file__)
            for cmd in Commands.scan(module):
                Commands.names[cmd.__name__] = cmd.__module__.split(".")[-1]
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
        event.reply(f"NAMES = {Json.dumps(Commands.names, indent=4, sort_keys=True)}")


def __dir__():
    return (
        'Cmd',
    )
