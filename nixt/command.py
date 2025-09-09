# This file is placed in the Public Domain.


"commands"


import inspect
import os


from .methods import parse


class Commands:

    cmds  = {}
    mod   = "mods"
    names = {}

    @staticmethod
    def add(func) -> None:
        Commands.cmds[func.__name__] = func
        Commands.names[func.__name__] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        evt.display()
    evt.ready()


def modules():
    if not os.path.exists(Commands.mod):
        return {}
    return sorted([
            x[:-3] for x in os.listdir(Commands.mod)
            if x.endswith(".py") and not x.startswith("__")
           ])


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def __dir__():
    return (
        'Commands',
        'command',
        'modules',
        'parse',
        'scan'
    )
