# This file is placed in the Public Domain.


"module management"


import inspect
import logging
import os


from .utility import Md5, Utils, e, j


class Mods:

    dirs = {}
    md5s = {}
    modules = {}

    @classmethod
    def add(cls, pkgname, path):
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
            fnm = j(path, name + ".py")
            if not e(fnm):
                continue
            if cls.md5s:
                md5 = Md5.md5(fnm)
                if md5 != cls.md5s.get(name):
                    logging.warning("mismatch %s", modname)
            return cls.importer(modname, fnm)

    @classmethod
    def getcmd(cls, name, cmd):
        mod = cls.get(name)
        func = getattr(mod, cmd, False)
        if not func:
            return
        if not inspect.isfunction(func):
            return
        if 'event' in inspect.signature(func).parameters:
            return func

    @classmethod
    def getcmds(cls, name):
        mod = cls.get(name)
        if not mod:
            return []
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in inspect.signature(cmdz).parameters:
                yield key

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
        return sorted(set(mods))

    @classmethod
    def table(cls):
        "read table,"
        try:
            from .statics import MODULES
            Mods.md5s.update(MODULES)
            return True
        except ImportError:
            return False


def __dir__():
    return (
        'Mods',
    )
