# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .objects import Methods
from .package import Mods
from .utility import Utils


class Commands:

    cmds = {}
    names = {}

    @classmethod
    def add(cls, *args):
        "add functions to commands."
        for func in args:
            cls.cmds[func.__name__] = func
            modname = func.__module__.split(".")[-1]
            if "__" in modname:
                continue
            cls.names[func.__name__] = modname

    @classmethod
    def command(cls, evt):
        "command callback."
        Methods.parse(evt, evt.text)
        func = cls.get(evt.cmd)
        if not func:
            name = cls.names.get(evt.cmd)
            mod = None
            if name:
                mod = Mods.get(name)
            if mod:
                cls.scan(mod)
                func = cls.get(evt.cmd)
        if func:
            if not cls.skip(func, evt.orig):
                func(evt)
                evt.display()
        evt.ready()

    @classmethod
    def commands(cls, orig):
        "list cpmmands available."
        res = []
        for func in cls.cmds.values():
            if cls.skip(func, orig):
                continue
            res.append(func.__name__)
        return res

    @classmethod
    def get(cls, cmd):
        "get function for command."
        return cls.cmds.get(cmd, None)

    @classmethod
    def scan(cls, module):
        "scan a module for functions with event as argument."
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' in inspect.signature(cmdz).parameters:
                cls.add(cmdz)

    @classmethod
    def scanner(cls):
        "scan named modules for commands."
        for name, mod in Mods.iter(Mods.list()):
            cls.scan(mod)

    @classmethod
    def skip(cls, func, orig):
        if "skip" in dir(func):
            for skp in Utils.spl(func.skip):
                if skp.lower() in orig.lower():
                    return True
        return False

    @classmethod
    def table(cls):
        mod = Mods.get("tbl")
        names = getattr(mod, "NAMES", None)
        if names:
            cls.names.update(names)


def __dir__():
    return (
        'Commands',
    )
