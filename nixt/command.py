# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .objects import Parse
from .package import Mods
from .utility import Utils


class Commands:

    cmds = {}
    names = {}

    @classmethod
    def add(cls, *args):
        "add functions to commands."
        for func in args:
            cls.cmds[func.__name__] = func
            modname = func.__module__.split(".")[-1]
            if "__" in modname:
                continue
            cls.names[func.__name__] = modname

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
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
        else:
            evt.ready()

    @classmethod
    def commands(cls, ignore=""):
        "list cpmmands available."
        return [x for x in cls.names if x not in Utils.spl(ignore)]

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


NAMES = {
    "atr": "rss",
    "cfg": "cfg",
    "cmd": "bsc",
    "dis": "mdl",
    "dne": "tdo",
    "dpl": "rss",
    "eml": "mbx",
    "err": "rss",
    "exp": "rss",
    "fie": "fnd",
    "flt": "flt",
    "fnd": "fnd",
    "imp": "rss",
    "log": "log",
    "lou": "sil",
    "man": "man",
    "mbx": "mbx",
    "mod": "bsc",
    "nme": "rss",
    "now": "mdl",
    "pth": "pth",
    "pwd": "pwd",
    "rem": "rss",
    "req": "req",
    "res": "rss",
    "rss": "rss",
    "sil": "sil",
    "slg": "slg",
    "srv": "adm",
    "syn": "rss",
    "tbl": "adm",
    "tdo": "tdo",
    "thr": "thr",
    "tmr": "tmr",
    "udp": "udp",
    "upt": "bsc",
    "ver": "bsc",
    "wdr": "adm",
    "wsd": "wsd"
}


Commands.names.update(NAMES)


def __dir__():
    return (
        'Commands',
    )
