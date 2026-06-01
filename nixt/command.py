# This file is placed in the Public Domain.


"write your own commands"


from .message import Message
from .package import Mods
from .parsers import Parse


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
    def cmd(cls, text):
        evt = Message()
        evt.kind = "command"
        evt.text = text
        Commands.command(evt)
        evt.wait()
        yield from evt.result

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
        func = Mods.getcmd(evt.mod, evt.mod)
        if not func:
            func = Mods.getcmd(evt.mod, evt.cmd)
            if func:
                splitted = evt.otxt.split()
                Parse.parse(evt, " ".join(splitted[1:]), True, True)
        if not func:
            cmds = list(Mods.getcmds(evt.mod))
            if cmds:
                evt.reply(f"{evt.mod} <{'|'.join(cmds)}>")
                evt.ready()
                return
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
    )
