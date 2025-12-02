# This file is placed in the Public Domain.


"write ypur own commands"


import inspect


from .brokers import display
from .methods import parse
from .package import mods


class Commands:

    cmds = {}
    names = {}

    @staticmethod
    def add(*args):
       for func in args:
            name = func.__name__
            Commands.cmds[name] = func
            Commands.names[name] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt, evt.text)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        display(evt)
    evt.ready()


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if 'event' not in inspect.signature(cmdz).parameters:
            continue
        Commands.add(cmdz)


def __dir__():
    return (
        'Commands',
        'command',
        'scan'
    )
