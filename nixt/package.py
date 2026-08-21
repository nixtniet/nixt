# This file is placed in the Public Domain.


"module management"


import logging
import os


from .hashing import Md5
from .utility import Utils


class Mods:

    core = {}
    dirs = {}
    md5s = {}
    mods = {}

    @classmethod
    def dir(cls, pkgname, path=None):
        "add module/patgh."
        if not pkgname:
            return
        pkgn = pkgname
        if path is None:
            path = pkgname
            pkgn = pkgname.split(os.sep)[-1]
        cls.dirs[pkgn] = path

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
                if not md5s:
                    logging.info("missing %s md5sum", modname)
                elif md5 != md5s:
                    logging.info("mismatch %s", modname)
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
        if not spec or not spec.loader:
            return None
        cls.mods[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mods[name])
        return cls.mods[name]

    @classmethod
    def list(cls):
        "comma seperated list of available modules."
        mods = []
        for pkgname, path in cls.dirs.items():
            if not os.path.exists(path):
                continue
            mods.extend(Utils.listdir(path))
        return sorted(set(mods))

    @classmethod
    def moddir(cls):
        "return package modules path."
        return os.path.join(Utils.where(Mods), "modules")

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

    @classmethod
    def table(cls):
        "read static tables."
        cls.statics()
        if cls.core:
            Md5.check(cls.core)


def __dir__():
    return (
        'Mods',
    )
