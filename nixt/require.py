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
    def cmd(message: Message) -> None:
        "show commands."
        check = len(Commands.cmds) > len(Commands.names)
        message.reply(",".join(sorted((check and Commands.cmds) or Commands.names)))

    @staticmethod
    def tbl(message: Message) -> None:
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
        message.reply("# This file is placed in the Public Domain.")
        message.reply("\n")
        message.reply('"tables"')
        message.reply("\n")
        message.reply("from typing import Dict")
        message.reply("\n")
        message.reply(f"CORE: Dict[str, str] = {JSON.dumps(core, indent=4, sort_keys=True)}")
        message.reply("\n")
        message.reply(f"MODULES: Dict[str, str] = {JSON.dumps(md5s, indent=4, sort_keys=True)}")
        message.reply("\n")
        message.reply(f"NAMES: Dict[str, str] = {JSON.dumps(Commands.names, indent=4, sort_keys=True)}")
        message.reply("\n")
        message.reply("def __dir__():")
        message.reply("    return (")
        message.reply("        'CORE',")
        message.reply("        'MODULES',")
        message.reply("        'NAMES'")
        message.reply("    )")

    @staticmethod
    def ver(message: Message) -> None:
        "show verson."
        message.reply(f"{Main.name.upper()} {MD5.core()}")


def __dir__():
    return (
        'Cmd',
    )
