# This file is placed in the Public Domain.


"write your own commands"


from .package import Mods
from .parsers import Parse


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
        func = Mods.getcmd(evt.mod, evt.cmd)
        if not func:
            func = cls.cmds.get(evt.mod)
        if not func:
            cmds = list(Mods.getcmds(evt.mod))
            if cmds:
                evt.reply(f"{evt.mod} <{'|'.join(cmds)}>")
        else:
            func(evt)
        evt.display()
        evt.ready()

    @classmethod
    def scan(cls, module):
        "scan a module for functions with event as argument."
        import inspect
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' in inspect.signature(cmdz).parameters:
                cls.add(cmdz)


def __dir__():
    return (
        'Commands',
    )
