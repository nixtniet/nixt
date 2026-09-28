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
    def cmd(msg: Message) -> None:
        "show commands."
        check = len(Commands.cmds) > len(Commands.names)
        msg.reply(",".join(sorted((check and Commands.cmds) or Commands.names)))

    @staticmethod
    def tbl(msg: Message) -> None:
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
        msg.reply("# This file is placed in the Public Domain.")
        msg.reply("\n")
        msg.reply('"tables"')
        msg.reply("\n")
        msg.reply("from typing import Dict")
        msg.reply("\n")
        msg.reply(f"CORE: Dict[str, str] = {JSON.dumps(core, indent=4, sort_keys=True)}")
        msg.reply("\n")
        msg.reply(f"MODULES: Dict[str, str] = {JSON.dumps(md5s, indent=4, sort_keys=True)}")
        msg.reply("\n")
        msg.reply(f"NAMES: Dict[str, str] = {JSON.dumps(Commands.names, indent=4, sort_keys=True)}")
        msg.reply("\n")
        msg.reply("def __dir__():")
        msg.reply("    return (")
        msg.reply("        'CORE',")
        msg.reply("        'MODULES',")
        msg.reply("        'NAMES'")
        msg.reply("    )")

    @staticmethod
    def ver(msg: Message) -> None:
        "show verson."
        msg.reply(f"{Main.name.upper()} {MD5.core()}")


def __dir__():
    return (
        'Cmd',
    )
