# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"write your own commands"


import inspect


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
        for _key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' not in inspect.signature(cmdz).parameters:
                continue
            self.add(cmdz)


def __dir__():
    return (
        'Command',
    )
