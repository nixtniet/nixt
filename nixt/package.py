# This file is placed in the Public Domain.


"module mamagement"


import importlib.util as imp
import os


from .persist import Workdir
from .utility import Utils


e = os.path.exists
j = os.path.join


class Mods:

    dirs = {}
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
    def configure(cls, cfg):
        "configure module directories."
        if cfg.user:
            if e("mods"): cls.add('mods', 'mods')
            if e("other"): cls.add("other", "other")
        cls.add("modules", j(Workdir.wdr, "mods"))
        cls.add(f"{Utils.pkgname(Mods)}.modules", Utils.moddir())

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


def __dir__():
    return (
        'Mods',
    )
