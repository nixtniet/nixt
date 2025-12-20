# This file is placed in the Public Domain.


"multiple directory modules"


import os


from .configs import Config
from .utility import importer, spl


class Mods:

    dirs = {}
    modules = {}
    package = __spec__.parent or ""
    path = os.path.dirname(__spec__.loader.path)


def dirs(name, path):
    Mods.dirs[name] = path


def mod(name):
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
    return [
            mod(x) for x in sorted(spl(names))
            if x not in spl(Config.ignore)
            or x in spl(Config.sets.init)]


def __dir__():
    return (
        'Mods',
        'dirs',
        'mod',
        'mods',
        'modules'
    )
