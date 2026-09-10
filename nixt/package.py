# This file is placed in the Public Domain.


"module management"


import logging
import os


from .objects import Method
from .utility import Utils


class Mods:

    "modules"

    core = {}
    dirs = {}
    md5s = {}
    mods = {}

    @classmethod
    def dir(cls, pkgname, path=None):
        "add module/path."
        if not pkgname:
            return
        pkgn = pkgname
        if path is None:
            path = pkgname
            pkgn = ".".join(pkgname.split(os.sep)[-2:])
        cls.dirs[pkgn] = path

    @classmethod
    def get(cls, name, force=False):
        "return module from cache or import module."
        for pkgname, path in cls.dirs.items():
            modname = f"{pkgname}.{name}"
            mod = cls.mods.get(modname, None)
            if mod:
                return mod
            fnm = os.path.join(path, name + ".py")
            if not os.path.exists(fnm):
                continue
            if not force and cls.md5s:
                md5 = MD5.md5(fnm)
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
    def minimal(cls):
        "return package minimal path."
        return os.path.join(Method.where(Mods), "minimal")

    @classmethod
    def moddir(cls):
        "return package modules path."
        return os.path.join(Method.where(Mods), "modules")

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
            MD5.check(cls.core)


class MD5:

    "module md5sums"

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
            if md5s and cls.md5(modpath) != md5s.get(name):
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
    def createmd5(cls, path, data):
        for pth in os.listdir(path):
            if pth.startswith("__") or not pth.endswith(".py") or "statics" in pth:
                continue
            name = pth[:-3]
            data[name] = cls.md5(os.path.join(path, pth))

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
        'MD5',
        'Mods'
    )
