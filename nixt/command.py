# This file is placed in the Public Domain.


"program your own commands"


import inspect
import logging
import os


from .brokers import Clients
from .encoder import Json
from .package import Mods
from .parsers import Parse
from .utility import Utils


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
        func = cls.cmds.get(evt.cmd, cls.ondemand(evt.cmd))
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
    def ondemand(cls, name):
        "ondemand loading of commands."
        modname = cls.names.get(name, None)
        if not modname:
            return
        mod = Mods.get(modname)
        if not mod:
            return
        logging.debug(f"load {modname}")
        cls.scan(mod)
        return cls.cmds.get(name, None)

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


def __dir__():
    return (
        'Cmd',
        'Commands'
    )
