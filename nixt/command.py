# This file is placed in the Public Domain.


"program your own commands"


import inspect
import logging
import os


from .brokers import Clients
from .encoder import Json
from .package import Mods
from .parsers import Parse
from .utility import Md5, Utils


class Commands:

    cmds = {}
    names = {}

    @classmethod
    def add(cls, *funcs):
        "register a command."
        for func in funcs:
            cls.cmds[func.__name__] = func

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
        func = cls.cmds.get(evt.cmd, None)
        if not func:
            modname = cls.names.get(evt.cmd, None)
            if not modname:
                return evt.ready()
            mod = Mods.get(modname)
            if not mod:
                evt.ready()
            logging.debug(f"load {modname}")
            cls.scan(mod)
            func = cls.cmds.get(evt.cmd, None)
        if func:
            func(evt)
            Clients.display(evt)
        evt.ready()

    @classmethod
    def list(cls, ignore=""):
        "scan for a list of all commands."
        result = []
        for modname in Mods.list(ignore):
            mod = Mods.get(modname)
            result.extend([x.__name__ for x in Commands.scan(mod, True) if x])
        return result

    @classmethod
    def scan(cls, mod, skip=False):
        "scan module for commands."
        result = []
        for nme, func in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in inspect.signature(func).parameters:
                if not skip:
                    cls.add(func)
                result.append(func)
        return result

    @classmethod
    def scanner(cls):
        "scan all modules."
        for name in Mods.list():
            cls.scan(Mods.get(name))

    @classmethod
    def statics(cls):
        "read table,"
        try:
            from .statics import NAMES
            cls.names.update(NAMES)
        except (ImportError, SyntaxError, ValueError):
            pass

    @classmethod
    def table(cls):
        "read static tables."
        cls.statics()
        if not cls.names:
            cls.scanner()


class Cmd:

    def cmd(event):
        "show commands."
        event.reply(",".join(sorted(Commands.names or Commands.cmds)))

    def tbl(event):
        "create table."
        core = {}
        md5s = {}
        Commands.names = {}
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
        event.reply(f"NAMES = {Json.dumps(Commands.names, indent=4, sort_keys=True)}")


def __dir__():
    return (
        'Cmd',
        'Commands'
    )
