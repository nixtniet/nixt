# This file is placed in the Public Domain.


"write your own commands"


import inspect
import logging


from .brokers import Broker
from .objects import Methods
from .package import Mods


class Commands:

    cmds = {}
    names = {}

    @staticmethod
    def add(*args):
        "add functions to commands."
        for func in args:
            name = func.__name__
            Commands.cmds[name] = func
            modname = func.__module__.split(".")[-1]
            if "__" in modname:
                continue
            Commands.names[name] = modname

    @staticmethod
    def command(evt):
        "command callback."
        Methods.parse(evt, evt.text)
        func = Commands.get(evt.cmd)
        if not func:
            name = Commands.names.get(evt.cmd)
            if name:
                logging.debug("load %s", name)
                mod = getattr(Mods.get(name))
                Commands.scan(mod)
                func = Commands.get(evt.cmd)
        if func:
            func(evt)
            bot = Broker.get(evt.orig)
            if bot:
                bot.display(evt)
        evt.ready()

    @staticmethod
    def get(cmd):
        "get function for command."
        return Commands.cmds.get(cmd, None)

    @staticmethod
    def has(cmd):
        "whether cmd is registered."
        return cmd in Commands.cmds

    @staticmethod
    def scan(module):
        "scan a module for functions with event as argument."
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' not in inspect.signature(cmdz).parameters:
                continue
            Commands.add(cmdz)

    @staticmethod
    def table():
        mod = Mods.get("tbl")
        if not mod:
            return
        names = getattr(mod, "NAMES", None)
        if names:
            Commands.names.update(names)


def __dir__():
    return (
        'Commands',
    )
