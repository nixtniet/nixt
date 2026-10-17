# This file is placed in the Public Domain.


"program your own commands"


import inspect


from .brokers import Clients
from .package import Mods
from .parsers import Parser
from .utility import Utils


class Commands:

    "command dispatch"

    cmds = {}
    names = {}

    @classmethod
    def add(cls, *funcs):
        "register a command."
        for func in funcs:
            name = Utils.funcname(func)
            cls.cmds[name] = func

    @classmethod
    def command(cls, msg):
        "command callback."
        Parser.parse(msg, msg.text)
        func = cls.cmds.get(msg.cmd, cls.ondemand(msg.cmd))
        if func:
            func(msg)
            Clients.display(msg)
        msg.ready()

    @classmethod
    def list(cls):
        "scan for a list of all commands."
        result = []
        for modname in Mods.list():
            mod = Mods.get(modname)
            if not mod:
                continue
            result.extend([Utils.funcname(x) for x in Commands.scan(mod, True)])
        return result

    @classmethod
    def ondemand(cls, name):
        "ondemand loading of commands."
        modname = cls.names.get(name, None)
        if not modname:
            return None
        mod = Mods.get(modname)
        if not mod:
            return None
        cls.scan(mod)
        return cls.cmds.get(name, None)

    @classmethod
    def scan(cls, mod, skip=False):
        "scan module for commands."
        result = []
        for nme, func in inspect.getmembers(mod, inspect.isfunction):
            if "cb_" in nme:
                continue
            if 'msg' in inspect.signature(func).parameters:
                if not skip:
                    cls.add(func)
                result.append(func)
        return result

    @classmethod
    def scanner(cls):
        "scan all modules."
        for name in Mods.list():
            mod = Mods.get(name)
            if not mod:
                continue
            cls.scan(mod)

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


def __dir__():
    return (
        'Commands',
    )
