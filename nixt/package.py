# This file is placed in the Public Domain.


"write your own commands"


import importlib.util as imp
import logging
import os


from .configs import Main, d, e, j
from .objects import Base
from .utility import Utils


class Mods:

    dirs = {f"{Utils.pkgname(Base)}.modules": j(d(__spec__.loader.path), "modules")}
    md5s = {}
    modules = {}

    @classmethod
    def add(cls, path, name=None):
        "add modules directory."
        if os.sep not in path:
            name = path
        elif name is None:
            name = path.split(os.sep)[-2]
        if e(path):
            cls.dirs[name] = path

    @classmethod
    def all(cls):
        "return all modules."
        return cls.iter(cls.list())

    @classmethod
    def get(cls, modname):
        "return module."
        mod = cls.modules.get(modname, None)
        if mod:
            return mod
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
    def iter(cls, mods=""):
        "loop over modules."
        has = []
        if Main.all and not mods:
            mods = Mods.list()
        for name in Utils.spl(mods or Main.mods):
            if name in Utils.spl(Main.ignore):
                continue
            if name in has:
                continue
            for pkgname, path in cls.dirs.items():
                fnm = j(path, name + ".py")
                if not e(fnm):
                    continue
                modname = f"{pkgname}.{name}"
                mod = cls.modules.get(modname, None)
                if not mod:
                    mod = cls.importer(modname, fnm)
                if mod:
                    has.append(name)
                    yield name, mod
                    break

    @classmethod
    def list(cls):
        "comma seperated list of available modules."
        mods = []
        for pkgname, path in cls.dirs.items():
            mods.extend([
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(Main.ignore)
            ])
        return ",".join(sorted(set(mods)))

    @classmethod
    def importer(cls, name, pth=""):
        "import module by path."
        if pth and e(pth):
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
        if "tbl" not in name:
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
            pth = j(path, name + ".py")
            if e(pth):
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


def __dir__():
    return (
        'Mods',
    )
