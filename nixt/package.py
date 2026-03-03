# This file is placed in the Public Domain.


"module management"


import importlib
import importlib.util
import logging
import os


from .utility import spl


class Mods:

    dirs = {}
    modules = {}

    def dir(self, name, path):
        "add modules directory." 
        if os.path.exists(path):
            self.dirs[name] = path

    def get(self, modname):
        "return module."
        result = list(self.iter(modname))
        if result:
            return result[0][-1]
        return None

    def has(self, attr):
        "return list of modules containing an attribute."
        result = []
        for mod in self.modules.values():
            if getattr(mod, attr, False):
                result.append(mod.__name__.split(".")[-1])
        return ",".join(result)

    def importer(self, name, pth=""):
        "import module by path."
        if pth and os.path.exists(pth):
            spec = importlib.util.spec_from_file_location(name, pth)
        else:
            spec = importlib.util.find_spec(name)
        if not spec or not spec.loader:
            logging.debug("missing spec or loader for %s", name)
            return None
        mod = importlib.util.module_from_spec(spec)
        if not mod:
            logging.debug("can't load %s module from spec", name)
            return None
        self.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod

    def iter(self, mods, ignore=""):
        "loop over modules."
        for pkgname, path in self.dirs.items():
            if not os.path.exists(path):
                continue
            for fnm in os.listdir(path):
                if fnm.startswith("__"):
                    continue
                if not fnm.endswith(".py"):
                    continue
                name = fnm[:-3]
                if name not in spl(mods):
                    continue
                if ignore and name in spl(ignore):
                    continue
                modname = f"{pkgname}.{name}"
                mod =  self.modules.get(modname, None)
                if not mod:
                    mod = self.importer(
                                        modname,
                                        os.path.join(path, fnm)
                                       )
                if mod:
                    yield name, mod

    def list(self, ignore=""):
        "comma seperated list of available modules."
        mods = []
        for _name, path in self.dirs.items():
            mods.extend([
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in spl(ignore)
            ])
        return ",".join(sorted(mods))

    def pkg(self, package):
        return self.dir(package.__name__, package.__path__[0])


"interface"


def __dir__():
    return (
        'Mods',
    )
