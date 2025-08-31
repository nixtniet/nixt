# This file is placed in the Public Domain.


"commands"


import inspect


from .clients import Fleet
from .kernels import Kernel


class Commands:

    cmds  = {}
    names = {}

    @staticmethod
    def add(func, module=None) -> None:
        Commands.cmds[func.__name__] = func
        if module:
            Commands.names[func.__name__] = module.__name__.split(".")[-1]

    @staticmethod
    def get(cmd):
        func = Commands.cmds.get(cmd, None)
        if not func:
            name = Commands.names.get(cmd, None)
            if not name:
                return
            module = Kernel.load(name)
            if module:
                Commands.scan(module)
                func = Commands.cmds.get(cmd)
        return func

    @staticmethod
    def command(evt):
        Commands.parse(evt)
        func = Commands.get(evt.cmd)
        if func:
            func(evt)
            Fleet.display(evt)
        evt.ready()

    @staticmethod
    def parse(obj, txt=None):
        if txt is None:
            if "txt" in dir(obj):
                txt = obj.txt
            else:
                txt = ""
        args = []
        obj.args   = []
        obj.cmd    = ""
        obj.gets   = {}
        obj.index  = None
        obj.mod    = ""
        obj.opts   = ""
        obj.result = {}
        obj.sets   = {}
        obj.silent = {}
        obj.txt    = txt or ""
        obj.otxt   = obj.txt
        _nr = -1
        for spli in obj.otxt.split():
            if spli.startswith("-"):
                try:
                    obj.index = int(spli[1:])
                except ValueError:
                    obj.opts += spli[1:]
                continue
            if "-=" in spli:
                key, value = spli.split("-=", maxsplit=1)
                obj.silent[key] = value
                obj.gets[key] = value
                continue
            if "==" in spli:
                key, value = spli.split("==", maxsplit=1)
                obj.gets[key] = value
                continue
            if "=" in spli:
                key, value = spli.split("=", maxsplit=1)
                if key == "mod":
                    if obj.mod:
                        obj.mod += f",{value}"
                    else:
                        obj.mod = value
                    continue
                obj.sets[key] = value
                continue
            _nr += 1
            if _nr == 0:
                obj.cmd = spli
                continue
            args.append(spli)
        if args:
            obj.args = args
            obj.txt  = obj.cmd or ""
            obj.rest = " ".join(obj.args)
            obj.txt  = obj.cmd + " " + obj.rest
        else:
            obj.txt = obj.cmd or ""

    @staticmethod
    def scan(module):
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz, module)

    @staticmethod
    def table():
        tbl = Kernel.load("tbl")
        names = getattr(tbl, "NAMES", None)
        if names:
            Commands.names.update(names)


def __dir__():
    return (
        'Commands',
    )
