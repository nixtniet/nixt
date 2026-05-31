# This file is placed in the Public Domain.


"write your own commands"


from .message import Message
from .package import Mods
from .parsers import Parse
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
        if not evt.text:
            evt.ready()
            return
        Parse.parse(evt, evt.text)
        mod = Mods.get(evt.mod)
        func = cls.cmds.get(evt.mod)
        if not func:
            cmds = getattr(mod, "Cmd", False)
            func = getattr(cmds, evt.cmd, False)
        if func:
            func(evt)
            evt.display()
        elif cmds:
            evt.reply(f"{evt.mod} <{'|'.join(Utils.skip(cmds))}>")
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
