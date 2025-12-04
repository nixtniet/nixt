# This file is placed in the Public Domain.


"multiple directory modules"


import os


from nixt.configs import Config
from nixt.utility import importer, spl
from nixt.workdir import Workdir


class Mods:

    dirs = {}
    modules = {}
    package = __spec__.parent or ""
    path = os.path.dirname(__spec__.loader.path)

    @staticmethod
    def add(name: str, path):
        Mods.dirs[name] = path

    @staticmethod
    def configure():
        name = Mods.package + ".modules" 
        Mods.add(name, os.path.join(Mods.path, "modules"))
        Mods.add("modules", Workdir.moddir())
        if "n" in Config.opts:
            name = Mods.package + ".network" 
            Mods.add(name, os.path.join(Mods.path, "network"))
        if "m" in Config.opts:
            Mods.add("mods", "mods")

    @staticmethod
    def get(name):
        if name in Mods.modules:
            return Mods.modules.get(name)
        mname = ""
        pth = ""
        for packname, path in Mods.dirs.items():
            modpath = os.path.join(path, name + ".py")
            if not os.path.exists(modpath):
                continue
            pth = modpath
            mname = f"{packname}.{name}"
            break
        if not mname:
            return
        mod = importer(mname, pth)
        if not mod:
            return
        Mods.modules[name] = mod
        return mod

    @staticmethod
    def list(ignore=""):
        mods = []
        for name, path in Mods.dirs.items():
            if name in spl(ignore):
                continue
            if not os.path.exists(path):
                continue
            mods.extend([
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and not x.startswith("__")
           ])
        return ",".join(sorted(mods))

    @staticmethod
    def mods(names):
        return [Mods.get(x) for x in sorted(spl(names))]


def __dir__():
    return (
        'Mods',
    )
