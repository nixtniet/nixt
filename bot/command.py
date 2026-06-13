# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .package import Mods
from .parsers import Parse


class Commands:

    cmds = {}

    @classmethod
    def add(cls, func):
        cls.cmds[func.__name__] = func

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
        func = cls.cmds.get(evt.cmd, None)
        if func:
            func(evt)
            evt.display()
        evt.ready()

    @classmethod
    def scan(cls, mod):
        for nme, func in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in inspect.signature(func).parameters:
                cls.add(func)


def __dir__():
    return (
        'Command',
    )
