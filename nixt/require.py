# This file is placed in the Public Domain.


"required commands"


import inspect
import os


from typing import Dict


from .command import Commands
from .configs import Main
from .encoder import JSON
from .message import Message
from .package import MD5, Mods
from .utility import Utils


class Cmd:

    "necessary commands."

    @staticmethod
    def cmd(event: Message) -> None:
        "show commands."
        check = len(Commands.cmds) > len(Commands.names)
        event.reply(",".join(sorted((check and Commands.cmds) or Commands.names)))

    @staticmethod
    def tbl(event: Message) -> None:
        "create table."
        core: Dict[str, str] = {}
        md5s: Dict[str, str] = {}
        Commands.names = {}
        if Main.mods:
            for name in Utils.spl(Main.mods):
                module = Mods.get(name, True)
                if not module:
                    continue
                if not module.__file__:
                    continue
                md5s[name] = MD5.md5(module.__file__)
                for cmd in Commands.scan(module):
                    Commands.names[cmd.__name__] = cmd.__module__.split(".")[-1]
        corepath = os.path.dirname(str(inspect.getsourcefile(Mods)))
        MD5.createmd5(corepath, core)
        event.reply("# This file is placed in the Public Domain.")
        event.reply("\n")
        event.reply('"tables"')
        event.reply("\n")
        event.reply("from typing import Dict")
        event.reply("\n")
        event.reply(f"CORE: Dict[str, str] = {JSON.dumps(core, indent=4, sort_keys=True)}")
        event.reply("\n")
        event.reply(f"MODULES: Dict[str, str] = {JSON.dumps(md5s, indent=4, sort_keys=True)}")
        event.reply("\n")
        event.reply(f"NAMES: Dict[str, str] = {JSON.dumps(Commands.names, indent=4, sort_keys=True)}")
        event.reply("\n")
        event.reply("def __dir__():")
        event.reply("    return (")
        event.reply("        'CORE',")
        event.reply("        'MODULES',")
        event.reply("        'NAMES'")
        event.reply("    )")

    @staticmethod
    def ver(event: Message) -> None:
        "show verson."
        event.reply(f"{Main.name.upper()} {MD5.core()}")


def __dir__():
    return (
        'Cmd',
    )
