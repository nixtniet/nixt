# This file is placed in the Public Domain.


"write your own commands"


import inspect


from nixt.brokers import display
from nixt.methods import parse


class Commands:

    cmds = {}
    names = {}


def addcmd(*args):
    for func in args:
        name = func.__name__
        Commands.cmds[name] = func
        Commands.names[name] = func.__module__.split(".")[-1]


def getcmd(cmd):
    return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt, evt.text)
    func = getcmd(evt.cmd)
    if func:
        func(evt)
        display(evt)
    evt.ready()


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if 'event' not in inspect.signature(cmdz).parameters:
            continue
        addcmd(cmdz)


def __dir__():
    return (
        'Commands',
        'addcmd',
        'getcmd',
        'command',
        'scan'
    )
