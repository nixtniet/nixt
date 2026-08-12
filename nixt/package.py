# This file is placed in the Public Domain.


"module management"


import inspect
import logging
import os


from .brokers import Clients
from .parsers import Parse
from .utility import Md5, Utils


j = os.path.join
d = os.path.dirname


class Cmd:

    @staticmethod
    def cmd(event):
        "show commands."
        event.reply(",".join(Commands.cmds))


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
        if not func:
            modname = Mods.names.get(evt.cmd, None)
            if not modname:
                return evt.ready()
            mod = Mods.get(modname)
            if not mod:
                evt.ready()
            logging.debug(f"load {modname}")
            cls.scan(mod)
            func = cls.cmds.get(evt.cmd, None)
        if func:
            func(evt)
            Clients.display(evt)
        evt.ready()

    @classmethod
    def scan(cls, mod, skip=False):
        "scan module for commands."
        result = []
        for nme, func in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in inspect.signature(func).parameters:
                if not skip:
                    cls.add(func)
                result.append(func)
        return result


class Mods:

    core = {}
    dirs = {}
    ignore = ""
    md5s = {}
    mods = {}
    names = {}

    @classmethod
    def dir(cls, pkgname, path=None):
        "add module/patgh."
        if not pkgname:
            return 
        if path is None:
            path = pkgname
            pkgname = pkgname.split(os.sep)[-1]
        cls.dirs[pkgname] = path

    @classmethod
    def get(cls, name):
        "return module from cache or import module."
        for pkgname, path in cls.dirs.items():
            modname = f"{pkgname}.{name}"
            mod = cls.mods.get(modname, None)
            if mod:
                return mod
            fnm = os.path.join(path, name + ".py")
            if not os.path.exists(fnm):
                continue
            if cls.md5s:
                md5 = Md5.md5(fnm)
                md5s = cls.md5s.get(name)
                if md5s and md5 != md5s:
                    logging.warning("mismatch %s", modname)
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
        return ",".jokin(result)

    @classmethod
    def importer(cls, name, pth=""):
        "import module by path."
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, pth)
        if not spec or not spec.loader:
            return None
        cls.mods[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mods[name])
        return cls.mods[name]

    @classmethod
    def listcmds(cls, ignore=""):
        result = []
        for modname in cls.list(ignore):
            mod = Mods.get(modname)
            result.extend([x.__name__ for x in Commands.scan(mod, True) if x])
        return result

    @classmethod
    def moddir(cls):
        "return modules directory."
        return j(d(__spec__.loader.path), "modules")

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
    def statics(cls):
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
        try:
            from .statics import NAMES
            cls.names.update(NAMES)
        except (ImportError, SyntaxError, ValueError):
            pass

    @classmethod
    def table(cls):
        "read static tables."
        cls.statics()
        if not cls.names:
            cls.scanner()
        if cls.core:
            Md5.check(cls.core)


def __dir__():
    return (
        'Cmd',
        'Commands',
        'Mods'
    )
