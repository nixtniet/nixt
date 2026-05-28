# This file is placed in the Public Domain.


"write your own commands"


import os


from .message import Message
from .parsers import Parse
from .utility import e, j


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
    def cmd(cls, text):
        evt = Message()
        evt.kind = "command"
        evt.text = text
        Commands.command(evt)
        evt.wait()
        yield from evt.result

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
        func = cls.get(evt.cmd)
        if func:
            func(evt)
            evt.display()
        evt.ready()

    @classmethod
    def get(cls, cmd):
        "get function for command."
        return cls.cmds.get(cmd, None)

    @classmethod
    def scan(cls, module):
        "scan a module for functions with event as argument."
        import inspect
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' in inspect.signature(cmdz).parameters:
                cls.add(cmdz)


class Mods:

    md5s = {}
    modules = {}

    @classmethod
    def has(cls, attr):
        "return list of modules containing an attribute."
        result = []
        for mod in cls.modules.values():
            if not getattr(mod, attr, False):
                continue
            result.append(mod.__name__.split(".")[-1])
        return ",".join(result)

    @classmethod
    def importer(cls, name, pth=""):
        "import module by path."
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, pth)
        cls.modules[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.modules[name])
        return cls.modules[name]

    @classmethod
    def scanner(cls, path):
        "scan named modules for commands."
        for name in os.listdir(path):
            if name.startswith("__") or not name.endswith(".py"):
                continue
            modname = path.split(os.sep)[-1] + "." + name[:-3]
            fnm = j(path, name)
            if not e(fnm):
                continue
            mod = cls.importer(modname, fnm)
            if not mod:
                continue
            if "configure" in dir(mod):
                mod.configure()
            Commands.scan(mod)


def __dir__():
    return (
        'Commands',
        'Mods'
    )
