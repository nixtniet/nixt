# This file is placed in the Public Domain.


"module management"


import inspect
import logging
import os


from .brokers import Clients
from .methods import Parse
from .utility import Utils


j = os.path.join
d = os.path.dirname


class Cmd:

    @staticmethod
    def cmd(event):
        "list available commands."
        event.reply(",".join(sorted(Mods.names or Mods.cmds)))


class Mods:

    cmds = {}

    core = {}
    dirs = {}
    md5s = {}
    mods = {}
    names = {}

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
            modname = cls.names.get(evt.cmd, None)
            if not modname:
                return evt.ready()
            mod = Mods.get(modname)
            if not mod:
                return evt.ready()
            logging.debug(f"load {modname}")
            cls.scan(mod)
            func = cls.cmds.get(evt.cmd, None)
        if func:
            func(evt)
            Clients.display(evt)
        evt.ready()

    @classmethod
    def configure(cls, name):
        cls.dir("modules", j(Utils.home(name), "mods"))
        cls.dir("mods", "mods")
        cls.table()

    @classmethod
    def dir(cls, pkgname, path):
        "add module/patgh."
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
        return ",".join(result)

    @classmethod
    def importer(cls, name, pth=""):
        "import module by path."
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, pth)
        cls.mods[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mods[name])
        return cls.mods[name]

    @classmethod
    def moddir(cls):
        "return modules directory."
        return os.path.join(os.path.dirname(os.path.dirname(__spec__.loader.path)), "modules")

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
    def scan(cls, mod):
        "scan module for commands."
        result = []
        for nme, func in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in inspect.signature(func).parameters:
                cls.add(func)
                result.append(func)
        return result

    @classmethod
    def scanner(cls):
        "scan all modules."
        for name in cls.list():
            cls.scan(cls.get(name))

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


class Md5:

    @classmethod
    def check(cls, md5s):
        "check for md5sums in a given path."
        ok = True
        path = os.path.dirname(__spec__.origin)
        if not os.path.exists(path):
            return False
        for pth in os.listdir(path):
            if pth.startswith("__") or not pth.endswith(".py") or "statics" in pth:
                continue
            name = pth[:-3]
            modpath = os.path.join(path, pth)
            if md5s and Md5.md5(modpath) != md5s.get(name):
                logging.warning("mismatch %s", name)
                ok = False
        return ok

    @classmethod
    def core(cls):
        "calculate md5 of the statics module."
        try:
            from . import statics
        except (ModuleNotFoundError, ImportError, SyntaxError):
            return ""
        return cls.source(Utils.source(statics))[:7].upper()

    @classmethod
    def dir(cls, path, md5):
        "create a md5 for a directory."
        for fnm in os.listdir(path):
            if not fnm.endswith(".py"):
                continue
            mpath = os.path.join(path, fnm)
            with open(mpath, "r", encoding="utf-8") as file:
                md5.update(file.read().encode("utf-8"))

    @classmethod
    def md5(cls, path):
        "calculate md5sum of a file."
        import hashlib
        md5 = hashlib.md5()
        with open(path, "r", encoding="utf-8") as file:
            md5.update(file.read().encode("utf-8"))
        return str(md5.hexdigest())

    @classmethod
    def source(cls, src):
        "determine md5 of source code."
        import hashlib
        md5 = hashlib.md5()
        md5.update(src.encode("utf-8"))
        return str(md5.hexdigest())


def __dir__():
    return (
        'Cmd',
        'Md5',
        'Mods'
    )
