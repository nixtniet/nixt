# This file is placed in the Public Domain.


"program your own commands"


import inspect


from collections.abc import Callable
from types           import ModuleType
from typing          import ClassVar, Dict, List, Union


from .clients import Clients
from .message import Message
from .package import Mods
from .parsers import Parser


class Commands:

    "command dispatch"

    cmds: ClassVar[Dict[str, Callable]] = {}
    names: ClassVar[Dict[str, str]] = {}

    @classmethod
    def add(cls, *funcs: Callable) -> None:
        "register a command."
        for func in funcs:
            if "__name__" not in dir(func):
                continue
            cls.cmds[func.__name__] = func

    @classmethod
    def command(cls, message: Message) -> None:
        "command callback."
        Parser.parse(message, message.text)
        func = cls.cmds.get(message.cmd, cls.ondemand(message.cmd))
        if func:
            func(message)
            Clients.display(message)
        message.ready()

    @classmethod
    def list(cls) -> Union[List[str]]:
        "scan for a list of all commands."
        result = []
        for modname in Mods.list():
            mod = Mods.get(modname)
            if not mod:
                continue
            result.extend([x.__name__ for x in Commands.scan(mod, True)])
        return result

    @classmethod
    def ondemand(cls, name: str) -> Union[Callable, None]:
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
    def scan(cls, mod: ModuleType, skip: bool = False) -> List[Callable]:
        "scan module for commands."
        result: List[Callable] = []
        for _nme, func in inspect.getmembers(mod, inspect.isfunction):
            if 'message' in inspect.signature(func).parameters:
                if not skip:
                    cls.add(func)
                result.append(func)
        return result

    @classmethod
    def scanner(cls) -> None:
        "scan all modules."
        for name in Mods.list():
            mod = Mods.get(name)
            if not mod:
                continue
            cls.scan(mod)

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
