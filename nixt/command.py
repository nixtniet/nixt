# This file is placed in the Public Domain.


"program your own commands"


import inspect


from collections.abc import Callable
from typing          import ClassVar, Dict, List


from .clients import Clients
from .package import Mods
from .parsers import Parser


class Commands:

    "command dispatch"

    cmds: ClassVar[Dict[str, Callable]] = {}
    names: ClassVar[Dict[str, str]] = {}

    @classmethod
    def add(cls, *funcs) -> None:
        "register a command."
        for func in funcs:
            cls.cmds[func.__name__] = func

    @classmethod
    def command(cls, evt) -> None:
        "command callback."
        Parser.parse(evt, evt.text)
        func = cls.cmds.get(evt.cmd, cls.ondemand(evt.cmd))
        if func:
            func(evt)
            Clients.display(evt)
        evt.ready()

    @classmethod
    def list(cls) -> List[str]:
        "scan for a list of all commands."
        result = []
        for modname in Mods.list():
            mod = Mods.get(modname)
            result.extend([x.__name__ for x in Commands.scan(mod, True) if x])
        return result

    @classmethod
    def ondemand(cls, name) -> Callable|None:
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
    def scan(cls, mod, skip=False) -> List[Callable]:
        "scan module for commands."
        result = []
        for _nme, func in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in inspect.signature(func).parameters:
                if not skip:
                    cls.add(func)
                result.append(func)
        return result

    @classmethod
    def scanner(cls) -> None:
        "scan all modules."
        for name in Mods.list():
            cls.scan(Mods.get(name))

    @classmethod
    def statics(cls) -> None:
        "read table,"
        try:
            from .statics import NAMES
            cls.names.update(NAMES)
        except (ImportError, SyntaxError, ValueError):
            pass

    @classmethod
    def table(cls) -> None:
        "read static tables."
        cls.statics()
        if not cls.names:
            cls.scanner()


def __dir__():
    return (
        'Commands',
    )
