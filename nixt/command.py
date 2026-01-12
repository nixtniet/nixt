# This file is placed in the Public Domain.


"write your commands"


import inspect


from .brokers import getobj
from .methods import parse
from .package import getmod
from .utility import spl


class Commands:

    cmds = {}
    names = {}


def addcmd(*args):
    "add functions to commands."
    for func in args:
        name = func.__name__
        Commands.cmds[name] = func
        Commands.names[name] = func.__module__.split(".")[-1]


def getcmd(cmd):
    "get function for command."
    func =  Commands.cmds.get(cmd, None)
    if func:
        return func
    name = Commands.names.get(cmd, None)
    if name:
        mod = getmod(name)
        if mod:
            scancmd(mod)
    return Commands.cmds.get(cmd, None)
        

def command(evt):
    "command callback."
    parse(evt, evt.text)
    func = getcmd(evt.cmd)
    if func:
        func(evt)
        bot = getobj(evt.orig)
        bot.display(evt)
    evt.ready()


def scancmd(module):
    "scan a module for functions with event as argument."
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if 'event' not in inspect.signature(cmdz).parameters:
            continue
        addcmd(cmdz)


def scanner(names):
    "scan named modules for commands."
    mods = []
    if Commands.names:
        return mods
    for name in spl(names):
        module = getmod(name)
        if not module:
            continue
        scancmd(module)
    return mods


def __dir__():
    return (
        'Commands',
        'addcmd',
        'command',
        'getcmd',
        'scancmd',
        'scanner'
    )
