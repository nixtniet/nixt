# This file is placed in the Public Domain.


"write your own commands"


import importlib.util as imp
import inspect
import logging
import os


from .objects import Method, Object
from .utility import Utils


e = os.path.exists
j = os.path.join


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

    @classmethod
    def table(cls):
        try:
            from .statics import NAMES
            cls.names.update(NAMES)
        except ImportError:
            pass


class Mods:

    core = {}
    dirs = {}
    md5s = {}
    modules = {}

    @classmethod
    def add(cls, name, path):
        "add modules directory."
        cls.dirs[name] = path

    @classmethod
    def all(cls):
        "return all modules."
        return cls.iter(cls.list())

    @classmethod
    def get(cls, name):
        "return module from cache or import module."
        for pkgname, path in cls.dirs.items():
            modname = f"{pkgname}.{name}"
            mod = cls.modules.get(modname, None)
            if not mod:
                fnm = j(path, name + ".py")
                if not e(fnm):
                    continue
                md5 = Utils.md5(fnm)
                if md5 != cls.md5s.get(name):
                    logging.warning("mismatch on module %s", name)
                mod = cls.importer(modname, fnm)
            return mod

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
    def iter(cls, mods="", ignore=""):
        "loop over modules."
        for name in Utils.spl(mods, ignore):
            mod = cls.get(name)
            if mod:
                yield name, mod

    @classmethod
    def list(cls, ignore=""):
        "comma seperated list of available modules."
        mods = []
        for pkgname, path in cls.dirs.items():
            if not e(path):
                continue
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
        spec = imp.spec_from_file_location(name, pth)
        cls.modules[name] = imp.module_from_spec(spec)
        spec.loader.exec_module(cls.modules[name])
        return cls.modules[name]

    @classmethod
    def path(cls, name):
        "return existing paths."
        for pkgname, path in cls.dirs.items():
            pth = j(path, name + ".py")
            if e(pth):
                return pth

    @classmethod
    def pkg(cls, *packages):
        "register packages their directories."
        for package in packages:
            cls.add(package.__path__[0], package.__name__)

    @classmethod
    def scanner(cls):
        "scan named modules for commands."
        if Commands.names:
            return
        for name in Utils.spl(cls.list()):
            mod = cls.get(name)
            Commands.scan(mod)

    @classmethod
    def table(cls):
        try:
            from .statics import NAMES, CORE, MD5
            Commands.names.update(NAMES)
            cls.core.update(CORE)
            cls.md5s.update(MD5)
        except ImportError:
            cls.scanner()


class Parse:

    @staticmethod
    def parse(obj, text):
        "parse text for command."
        data = {
            "args": [],
            "cmd": "",
            "gets": Object(),
            "index": None,
            "init": "",
            "opts": "",
            "otxt": text,
            "rest": "",
            "silent": Object(),
            "sets": Object(),
            "text": text
        }
        for k, v in data.items():
            setattr(obj, k, getattr(obj, k, v) or v)
        args = []
        nr = -1
        for spli in text.split():
            if spli.startswith("-"):
                try:
                    obj.index = int(spli[1:])
                except ValueError:
                    obj.opts += spli[1:]
                continue
            if "-=" in spli:
                key, value = spli.split("-=", maxsplit=1)
                Method.typed(obj.silent, key, value)
                Method.typed(obj.gets, key, value)
                continue
            if "==" in spli:
                key, value = spli.split("==", maxsplit=1)
                Method.typed(obj.gets, key, value)
                continue
            if "=" in spli:
                key, value = spli.split("=", maxsplit=1)
                Method.typed(obj.sets, key, value)
                continue
            nr += 1
            if nr == 0:
                obj.cmd = spli
                continue
            args.append(spli)
        if args:
            obj.args = args
            obj.text = obj.cmd or ""
            obj.rest = " ".join(obj.args)
            obj.text = obj.cmd + " " + obj.rest
        else:
            obj.text = obj.cmd or ""
        Method.notset(obj, obj.sets)


def __dir__():
    return (
        'Commands',
        'Mods'
    )
