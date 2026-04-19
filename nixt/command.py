# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .configs import Main
from .objects import Methods
from .package import Mods
from .utility import Utils


class Commands:

    allows = {}
    cmds = {}
    names = {}

    @classmethod
    def add(cls, *args):
        "add functions to commands."
        for func in args:
            name = func.__name__
            cls.cmds[name] = func
            modname = func.__module__.split(".")[-1]
            if "__" in modname:
                continue
            cls.names[name] = modname
            if "allow" in dir(func):
                cls.allows[name] = func.allow

    @classmethod
    def allow(cls, cmd, txt):
        "check whether to skip a command."
        alw = cls.allows.get(cmd, None)
        if not alw:
            return True
        if Main.admin and "admin" not in alw:
            return False
        for ok in Utils.spl(alw):
            if ok.lower() in txt.lower():
                return True
            return False
        return True

    @classmethod
    def command(cls, evt):
        "command callback."
        Methods.parse(evt, evt.text)
        if cls.allows.get(evt.cmd):
            if not cls.allow(evt.cmd, evt.orig):
                evt.ready()
                return
        func = cls.get(evt.cmd)
        if not func:
            name = cls.names.get(evt.cmd)
            mod = None
            if name:
                mod = Mods.get(name)
            if mod:
                cls.scan(mod)
                func = cls.get(evt.cmd)
        if func:
            func(evt)
            evt.display()
        evt.ready()

    @classmethod
    def commands(cls, orig):
        "list cpmmands available."
        res = []
        for nme in cls.names:
            if Main.admin and name not in Utils.spl(cls.admin):
                continue
            alw = cls.allows.get(nme, False)
            if alw and not cls.allow(nme, orig):
                continue
            res.append(nme)
        return res

    @classmethod
    def get(cls, cmd):
        "get function for command."
        return cls.cmds.get(cmd, None)

    @classmethod
    def scan(cls, module):
        "scan a module for functions with event as argument."
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' in inspect.signature(cmdz).parameters:
                cls.add(cmdz)

    @classmethod
    def table(cls):
        "load names from table."
        mod = Mods.get("tbl")
        names = getattr(mod, "NAMES", None)
        if names:
            cls.names.update(names)
        alw = getattr(mod, "ALLOWS", None)
        if alw:
            cls.allows.update(alw)


def __dir__():
    return (
        'Commands',
    )
