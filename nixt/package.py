# This file is placed in the Public Domain.


"module management"


import importlib.util
import logging
import os


from .utility import Utils


class Mods:

    dirs = {}
    md5s = {}
    modules = {}

    @classmethod
    def add(cls, name, path):
        "add modules directory."
        if os.path.exists(path):
            cls.dirs[name] = path

    @classmethod
    def all(cls):
        return cls.iter(cls.list())

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
    def iter(cls, modlist, ignore=""):
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
                if not mod:
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
            spec = importlib.util.spec_from_file_location(name, pth)
        else:
            spec = importlib.util.find_spec(name)
        if not spec or not spec.loader:
            logging.debug("missing spec or loader for %s", name)
            return None
        md5 = cls.md5s.get(name)
        md5sum = Utils.md5sum(spec.loader.path)
        if md5 and md5sum != md5:
            logging.error("mismatch %s", spec.loader.path)
        cls.md5s[name] = md5sum
        mod = importlib.util.module_from_spec(spec)
        if not mod:
            logging.debug("can't load %s module", name)
            return None
        cls.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod

    @classmethod
    def path(cls, name):
        for pkgname, path in cls.dirs.items():
            pth = os.path.join(path, name + ".py")
            if os.path.exists(pth):
                return pth

    @classmethod
    def pkg(cls, package):
        return cls.add(package.__name__, package.__path__[0])

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
