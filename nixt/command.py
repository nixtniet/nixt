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
    "srv": "adm",
    "tbl": "adm",
    "wdr": "adm",
    "cmd": "bsc",
    "mod": "bsc",
    "upt": "bsc",
    "ver": "bsc",
    "cfg": "cfg",
    "flt": "flt",
    "fie": "fnd",
    "fnd": "fnd",
    "log": "log",
    "man": "man",
    "eml": "mbx",
    "mbx": "mbx",
    "dis": "mdl",
    "now": "mdl",
    "pth": "pth",
    "pwd": "pwd",
    "req": "req",
    "atr": "rss",
    "dpl": "rss",
    "err": "rss",
    "exp": "rss",
    "imp": "rss",
    "nme": "rss",
    "rem": "rss",
    "res": "rss",
    "rss": "rss",
    "syn": "rss",
    "lou": "sil",
    "sil": "sil",
    "slg": "slg",
    "dne": "tdo",
    "tdo": "tdo",
    "thr": "thr",
    "tmr": "tmr",
    "udp": "udp",
    "wsd": "wsd"
}


Commands.names.update(NAMES)


def __dir__():
    return (
        'Commands',
    )
