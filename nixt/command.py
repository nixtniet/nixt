# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .package import Mods
from .parsers import Parse
from .utility import Utils


class Commands:

    cmds = {}

    @classmethod
    def add(cls, *args):
        "add functions to commands."
        for func in args:
            cls.cmds[func.__name__] = func

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
        func = cls.get(evt.cmd)
        if not func:
            name = Mods.names.get(evt.cmd)
            mod = None
            if name:
                mod = Mods.get(name)
            if mod:
                cls.scan(mod)
                func = cls.get(evt.cmd)
        if func:
            func(evt)
            evt.display()
        evt.ready()

    @classmethod
    def commands(cls, ignore=""):
        "list cpmmands available."
        return [x for x in cls.names if x not in Utils.spl(ignore)]

    @classmethod
    def get(cls, name):
        "get function for command."
        return cls.cmds.get(name, None)

    @classmethod
    def scan(cls, module):
        "scan a module for functions with event as argument."
        import inspect
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' in inspect.signature(cmdz).parameters:
                cls.add(cmdz)

    @classmethod
    def scanner(cls):
        "scan named modules for commands."
        for name in Mods.list():
            mod = Mods.get(name)
            if not mod:
                continue
            if "configure" in dir(mod):
                mod.configure()
            cls.scan(mod)

    @classmethod
    def table(cls):
        "read table,"
        try:
            from .statics import NAMES
            cls.names.update(NAMES)
            return True
        except ImportError:
            return False


def __dir__():
    return (
        'Commands',
        'cmd'
    )
