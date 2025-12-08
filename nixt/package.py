# This file is placed in the Public Domain.


"multiple directory modules"


import os


from .workdir import moddir
from .utility import importer, spl


class Mods:

    dirs = {}
    modules = {}
    package = __spec__.parent or ""
    path = os.path.dirname(__spec__.loader.path)


def adddir(name: str, path):
    Mods.dirs[name] = path


def confmod(local=False, network=False):
    name = Mods.package + ".modules" 
    adddir(name, os.path.join(Mods.path, "modules"))
    adddir("modules", moddir())
    if network:
        name = Mods.package + ".network" 
        adddir(name, os.path.join(Mods.path, "network"))
    if local:
        adddir("mods", os.path.join(os.getcwd(), "mods"))


def getmod(name):
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


def modules(ignore=""):
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
    return ",".join(sorted(mods)).strip()


def mods(names):
    return [getmod(x) for x in sorted(spl(names))]


def __dir__():
    return (
        'Mods',
        'adddir',
        'confmod',
        'getmod',
        'modules',
        'mods'
    )
