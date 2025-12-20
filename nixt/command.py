# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .methods import parse


class Commands:

    cmds = {}
    names = {}


def enable(*args):
    for func in args:
        name = func.__name__
        Commands.cmds[name] = func
        Commands.names[name] = func.__module__.split(".")[-1]


def cmds(cmd):
    return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt, evt.text)
    func = cmds(evt.cmd)
    if func:
        func(evt)
        evt.display()
    evt.ready()


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if 'event' not in inspect.signature(cmdz).parameters:
            continue
        enable(cmdz)


def __dir__():
    return (
        'Commands',
        'command',
        'cmds',
        'enable',
        'scan'
    )
