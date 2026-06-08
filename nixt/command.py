# This file is placed in the Public Domain.


"write your own commands"


import inspect
import logging
import os


from .package import Mods
from .parsers import Parse
from .threads import Thread
from .utility import Md5, Utils, e, j


class Commands:

    completions = []

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
        func = cls.getcmd(evt.mod, evt.cmd)
        if not func:
            func = cls.find(evt.cmd)
        if func:
            func(evt)
            evt.display()
        evt.ready()

    @classmethod
    def commands(cls):
        return [x.split(".")[-1] for x in cls.completions]

    @classmethod
    def find(cls, name):
        modname = ""
        for nme in cls.completions:
            try:
                mod, cmd = nme.split(".")
            except ValueError:
                continue
            if cmd == name:
                modname = mod
        if not modname:
            for nme in Mods.list():
                if name in cls.getcmds(nme):
                    modname = nme
        return cls.getcmd(modname, name)

    @classmethod
    def getcmd(cls, name, cmd):
        "return command."
        mod = Mods.get(name)
        func = getattr(mod, cmd, False)
        if not func:
            return
        if not inspect.isfunction(func):
            return
        if 'event' in inspect.signature(func).parameters:
            return func

    @classmethod
    def getcmds(cls, name):
        "return whitelist."
        mod = Mods.get(name)
        return getattr(mod, 'whitelist', [])

    @classmethod
    def scanner(cls):
        for name in Mods.list():
            for cmd in cls.getcmds(name):
                cls.completions.append(f"{name}.{cmd}")

    @classmethod
    def table(cls):
        "read table,"
        try:
            from .statics import COMPLETIONS, CORE, MODULES
            cls.completions = COMPLETIONS
        except (ImportError, SyntaxError, ValueError):
            logging.warn("running scanner")
            cls.scanner()


def __dir__():
    return (
        'Command',
    )
