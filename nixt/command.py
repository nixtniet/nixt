# This file is placed in the Public Domain.


"write your own commands"


import importlib.util as imp
import inspect
import logging
import os
import threading
import time


from .objects import Data, Methods
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
        Methods.parse(evt, evt.text)
        func = cls.get(evt.cmd)
        if func:
            func(evt)
            evt.display()
        evt.ready()

    @classmethod
    def commands(cls, orig):
        "list cpmmands available."
        res = []
        for func in cls.cmds.values():
            if cls.skip(func, orig): continue
            res.append(func.__name__)
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
    def scanner(cls):
        "scan named modules for commands."
        for name, mod in Mods.iter(Mods.list()):
            cls.scan(mod)

    @classmethod
    def skip(cls, func, orig):
        if "skip" in dir(func):
            for skp in Utils.spl(func.skip):
                if skp.lower() in orig.lower():
                    return True
        return False

    @classmethod
    def table(cls):
        mod = cls.get("tbl")
        names = getattr(mod, "NAMES", None)
        if names: cls.names.update(names)


class Mods:

    dirs = {}
    md5s = {}
    modules = {}

    @classmethod
    def add(cls, path, name=None):
        "add modules directory."
        if os.sep not in path:
            name = path
        elif name is None:
            name = path.split(os.sep)[-2]
        if os.path.exists(path):
            cls.dirs[name] = path
        print(cls.dirs)

    @classmethod
    def all(cls, force=False):
        "return all modules."
        return cls.iter(cls.list(), force=force)

    @classmethod
    def get(cls, modname):
        "return module."
        result = list(cls.iter(modname))
        if result:
            return result[0][-1]

    @classmethod
    def has(cls, attr):
        "return list of modules containing an attribute."
        result = []
        for mod in cls.modules.values():
            if getattr(mod, attr, False):
                result.append(mod.__name__.split(".")[-1])
        return ",".join(result)

    @classmethod
    def iter(cls, modlist, ignore="", force=False):
        "loop over modules."
        has = []
        for name in Utils.spl(modlist):
            if ignore and name in Utils.spl(ignore):
                continue
            if name in has:
                continue
            for pkgname, path in cls.dirs.items():
                fnm = os.path.join(path, name + ".py")
                if not os.path.exists(fnm):
                    continue
                modname = f"{pkgname}.{name}"
                mod = cls.modules.get(modname, None)
                if force or not mod:
                    mod = cls.importer(modname, fnm)
                if mod:
                    has.append(name)
                    yield name, mod
                    break

    @classmethod
    def list(cls, ignore=""):
        "comma seperated list of available modules."
        mods = []
        for pkgname, path in cls.dirs.items():
            mods.extend([
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(ignore)
            ])
        return ",".join(sorted(set(mods)))

    @classmethod
    def importer(cls, name, pth=""):
        "import module by path."
        if pth and os.path.exists(pth):
            spec = imp.spec_from_file_location(name, pth)
        else:
            spec = imp.find_spec(name)
        if not spec or not spec.loader:
            logging.debug("%s is missing spec or loader", name)
            return None
        md5 = cls.md5s.get(name)
        md5sum = Utils.md5sum(spec.loader.path)
        if md5 and md5sum != md5:
            logging.info("mismatch %s", spec.loader.path)
        cls.md5s[name] = md5sum
        mod = imp.module_from_spec(spec)
        if not mod:
            logging.debug("can't load %s module", name)
            return None
        cls.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod

    @classmethod
    def path(cls, name):
        "return existing paths."
        for pkgname, path in cls.dirs.items():
            pth = os.path.join(path, name + ".py")
            if os.path.exists(pth):
                return pth

    @classmethod
    def pkg(cls, *packages):
        "register packages their directories."
        for package in packages:
            cls.add(package.__path__[0], package.__name__)

    @classmethod
    def sums(cls):
        mod = cls.get("tbl")
        if not mod:
            return
        md5s = getattr(mod, "MD5", {})
        if not md5s:
            return
        cls.md5s.update(md5s)


class MainConfig(type):

    def __getattr__(cls, key):
        if key not in dir(cls):
            return ""
        return cls.__getattribute__(key)

    def __str__(cls):
        return str(Methods.skip(cls.__dict__))


class Main(metaclass=MainConfig):

    level = "info"
    name = Utils.pkgname(MainConfig)
    wdr = f".{name}"


def __dir__():
    return (
        'Commands',
        'Main',
        'Mods'
    )
