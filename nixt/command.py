# This file is placed in the Public Domain.


"write your own commands"


import inspect
import logging


from .brokers import Broker
from .methods import Methods
from .package import Mods


class Commands:

    cmds = {}
    names = {}

    @classmethod
    def add(cls, *args):
        "add functions to commands."
        for func in args:
            name = func.__name__
            cls.cmds[name] = func
            modname = func.__module__.split(".")[-1]
            if "__" in modname:
                continue
            cls.names[name] = modname

    @classmethod
    def command(cls, evt):
        "command callback."
        Methods.parse(evt, evt.text)
        func = cls.get(evt.cmd)
        if not func:
            name = cls.names.get(evt.cmd)
            mod = None
            if name:
                logging.debug("load %s", name)
                mod = Mods.get(name)
            if mod:
                cls.scan(mod)
                func = cls.get(evt.cmd)
        if func:
            func(evt)
            bot = Broker.get(evt.orig)
            if bot:
                bot.display(evt)
        evt.ready()

    @classmethod
    def get(cls, cmd):
        "get function for command."
        return cls.cmds.get(cmd, None)

    @classmethod
    def has(cls, cmd):
        "whether cmd is registered."
        return cmd in cls.cmds

    @classmethod
    def scan(cls, module):
        "scan a module for functions with event as argument."
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' not in inspect.signature(cmdz).parameters:
                continue
            cls.add(cmdz)

    @classmethod
    def table(cls):
        mod = cls.get("tbl")
        names = getattr(mod, "NAMES", None)
        if names:
            cls.names.update(names)


def __dir__():
    return (
        'Commands',
    )
