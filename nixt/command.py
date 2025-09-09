# This file is placed in the Public Domain.


"commands"


import inspect
import os


class Commands:

    cmds  = {}
    mod   = "mods"
    names = {}

    @staticmethod
    def add(func) -> None:
        Commands.cmds[func.__name__] = func
        Commands.names[func.__name__] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)


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


def parse(obj, txt=None):
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args   = getattr(obj, "args", [])
    obj.cmd    = getattr(obj, "cmd", "")
    obj.gets   = getattr(obj, "gets", "")
    obj.index  = getattr(obj, "index", None)
    obj.mod    = getattr(obj, "mod", "")
    obj.opts   = getattr(obj, "opts", "")
    obj.result = getattr(obj, "result", "")
    obj.sets   = getattr(obj, "sets", {})
    obj.silent = getattr(obj, "silent", "")
    obj.txt    = txt or getattr(obj, "txt", "")
    obj.otxt   = obj.txt or getattr(obj, "otxt", "")
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


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def __dir__():
    return (
        'Commands',
        'command',
        'modules',
        'parse',
        'scan'
    )
