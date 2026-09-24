# This file is placed in the Public Domain.


"program your own commands"


import inspect


from collections.abc import Callable
from typing          import ClassVar, Dict, List, Union
from types           import FunctionType


from .clients import Clients
from .message import Message
from .package import Mods
from .parsers import Parser


class Commands:

    "command dispatch"

    cmds: ClassVar[Dict[str, FunctionType]] = {}
    names: ClassVar[Dict[str, str]] = {}

    @classmethod
    def add(cls, *funcs: FunctionType) -> None:
        "register a command."
        for func in funcs:
            cls.cmds[func.__name__] = func

    @classmethod
    def command(cls, event: Message) -> None:
        "command callback."
        Parser.parse(event, event.text)
        func = cls.cmds.get(event.cmd, cls.ondemand(event.cmd))
        if func:
            func(event)
            Clients.display(event)
        event.ready()

    @classmethod
    def list(cls) -> Union[List[str] | None]:
        "scan for a list of all commands."
        result = []
        for modname in Mods.list():
            mod = Mods.get(modname)
            result.extend([x.__name__ for x in Commands.scan(mod, True)])
        return result

    @classmethod
    def ondemand(cls, name: str) -> Union[FunctionType, None]:
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
    def scan(cls, mod, skip=False) -> List[FunctionType]:
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
