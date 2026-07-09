# This file is placed in the Public Domain.


"module management"


import inspect
import logging
import os


from .configs import Main
from .parsers import Parse
from .utility import Md5, Utils


class Cmd:

    @classmethod
    def cmd(cls, event):
        "list available commands."
        event.reply(",".join(sorted(Commands.cmds)))


class Commands:

    cmds = {}

    @classmethod
    def add(cls, *funcs):
        "register a command."
        for func in funcs:
            cls.cmds[func.__name__] = func

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
        func = cls.cmds.get(evt.cmd, None)
        if func:
            func(evt)
            evt.display()
        evt.ready()

    @classmethod
    def scan(cls, mod):
        "scan module for commands."
        for nme, func in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in inspect.signature(func).parameters:
                cls.add(func)


class Mods:

    core = {}
    dirs = {}
    md5s = {}
    modules = {}

    @classmethod
    def dir(cls, pkgname, path):
        "add module/patgh."
        cls.dirs[pkgname] = path

    @classmethod
    def get(cls, name):
        "return module from cache or import module."
        for pkgname, path in cls.dirs.items():
            modname = f"{pkgname}.{name}"
            mod = cls.modules.get(modname, None)
            if mod:
                return mod
            fnm = os.path.join(path, name + ".py")
            if not os.path.exists(fnm):
                continue
            if cls.md5s:
                md5 = Md5.md5(fnm)
                md5s = cls.md5s.get(name)
                if md5s and md5 != md5s:
                    logging.warn("mismatch %s", modname)
            return cls.importer(modname, fnm)

    @classmethod
    def has(cls, attr):
        "return list of modules containing an attribute."
        result = []
        for modname in cls.list():
            mod = cls.get(modname)
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
    def list(cls, ignore=""):
        "comma seperated list of available modules."
        mods = []
        for pkgname, path in cls.dirs.items():
            if not os.path.exists(path):
                continue
            mods.extend(Utils.listdir(path, ignore))
        return sorted(set(mods))

    @classmethod
    def scanner(cls):
        "scan all modules."
        for name in cls.list():
            Commands.scan(cls.get(name))

    @classmethod
    def sums(cls):
        "read table,"
        try:
            from .statics import CORE
            cls.core.update(CORE)
        except (ImportError, SyntaxError, ValueError):
            pass
        try:
            from .statics import MODULES
            cls.md5s.update(MODULES)
        except (ImportError, SyntaxError, ValueError):
            pass


def __dir__():
    return (
        "Cmd",
        "Commands",
        'Mods'
    )
