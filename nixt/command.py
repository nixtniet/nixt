# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .message import Message
from .methods import parse


class Commands:

    cmds = {}
    names = {}

    def add(self, *args):
        "add functions to commands."
        for func in args:
            name = func.__name__
            self.cmds[name] = func
            self.names[name] = func.__module__.split(".")[-1]

    def get(self, cmd):
        "get function for command."
        return self.cmds.get(cmd, None)

    def has(self, cmd):
        "whether cmd is registered."
        return cmd in self.cmds

    def scan(self, module):
        "scan a module for functions with event as argument."
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' not in inspect.signature(cmdz).parameters:
               continue
            self.add(cmdz)


"interface"


def __dir__():
    return (
        'Command',
    )
