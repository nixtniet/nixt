# This file is placed in the Public Domain.


"commands"


import inspect


from .handler import Fleet
from .methods import parse, spl


class Commands:

    cmds  = {}
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
        Fleet.display(evt)
    evt.ready()


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
        'scan'
    )
