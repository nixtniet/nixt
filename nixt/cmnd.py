# This file is placed in the Public Domain.


"command"


import inspect
import os


from .config import Default
from .fleet  import Fleet
from .parse  import parse
from .path   import Workdir, skel
from .run    import launch
from .utils  import spl


class Main(Default):

    init = ""
    level = "warn"
    name = Default.__module__.split(".")[-2]
    opts = Default()


class Commands:

    cmds = {}
    names = {}

    @staticmethod
    def add(func, mod=None):
        Commands.cmds[func.__name__] = func
        if mod:
            Commands.names[func.__name__] = mod.__name__.split(".")[-1]

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)

    @staticmethod
    def scan(mod):
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if "event" in cmdz.__code__.co_varnames:
                Commands.add(cmdz, mod)


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if not func:
        evt.ready()
        return
    func(evt)
    Fleet.display(evt)
    evt.ready()


def inits(pkg, names):
    modz = []
    for name in sorted(spl(names)):
        mod = getattr(pkg, name, None)
        if not mod:
            continue
        if "init" in dir(mod):
            thr = launch(mod.init)
            modz.append((mod, thr))
    return modz


def scan(pkg):
    for modname in dir(pkg):
        mod = getattr(pkg, modname)
        Commands.scan(mod)


def setwd(name, path=""):
    Main.name = name
    path = path or os.path.expanduser(f"~/.{name}")
    Workdir.wdr = path
    skel()


"interface"


def __dir__():
    return (
        "Commands",
        "Main",
        "command",
        "scan",
        "setwd"
    )
