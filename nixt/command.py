# This file is placed in the Public Domain.


"commands"


import importlib.util
import inspect
import os


from .brokers import getobj
from .methods import parse
from .threads import launch
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


def command(evt):
    "command callback."
    parse(evt, evt.text)
    func = getcmd(evt.cmd)
    if func:
        func(evt)
        bot = getobj(evt.orig)
        bot.display(evt)
    evt.ready()


def getcmd(cmd):
    "get function for command."
    return Commands.cmds.get(cmd, None)
        

def importer(name, pth=""):
    "import module by path."
    if pth and os.path.exists(pth):
        spec = importlib.util.spec_from_file_location(name, pth)
    else:
        spec = importlib.util.find_spec(name)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    if not mod:
        return None
    spec.loader.exec_module(mod)
    return mod


def modules(*pkgs, ignore=""):
    "comma seperated list of available modules."
    mods = []
    for pkg in pkgs:
        path = pkg.__path__[0]
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and
            not x.startswith("__") and
            x[:-3] not in spl(ignore)
        ])
    return ",".join(sorted(mods))


def scancmd(module):
    "scan a module for functions with event as argument."
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if 'event' not in inspect.signature(cmdz).parameters:
            continue
        addcmd(cmdz)


def scanner(*pkgs, inits=""):
    "scan named modules for commands."
    mods = []
    for pkg in pkgs:
        if not pkg:
            continue
        path = pkg.__path__[0]
        for fnm in os.listdir(path):
            if fnm.startswith("__"):
                continue
            name = fnm[:-3]
            modname = f"{pkg.__name__}.{name}"
            mod = importer(modname, os.path.join(path, fnm))
            if not mod:
                continue
            scancmd(mod)
            if name not in spl(inits):
                continue
            if "init" not in dir(mod):
                continue
            launch(mod.init)
    return mods


def __dir__():
    return (
        'Commands',
        'addcmd',
        'command',
        'getcmd',
        'importer',
        'modules',
        'scancmd',
        'scanner'
    )
