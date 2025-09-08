# This file is placed in the Public Domain.


"commands"


import inspect
import os


from .methods import importer, parse, spl


class Commands:

    cmds   = {}
    mod = "mods"
    names  = {}

    @staticmethod
    def add(func) -> None:
        Commands.cmds[func.__name__] = func
        Commands.names[func.__name__] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd):
        func = Commands.cmds.get(cmd, None)
        if not func:
            name = Commands.names.get(cmd, None)
            if not name:
                return
            module = importer(name, Commands.mod)
            if module:
                scan(module)
                func = Commands.cmds.get(cmd)
        return func


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


def scanner(names=None, debug=False):
    res = []
    for nme in sorted(modules()):
        if names and nme not in spl(names):
            continue
        module = importer(nme, Commands.mod)
        if not module:
            continue
        scan(module)
        if debug and "DENUG" in dir(module):
            module.DEBUG = True
        res.append(module)
    return res


def table():
    tbl = importer("tbl", Commands.mod)
    if tbl:
        Commands.names.update(tbl.NAMES)
    else:
        scanner()


def __dir__():
    return (
        'Commands',
        'command',
        'scan'
    )
