# This file is placed in the Public Domain.


"module management."


import importlib.util
import os


from .configs import Config
from .utility import spl
from .workdir import moddir


class Mods:

    dirs = {}
    modules = {}
    package = __spec__.parent or ""
    path = os.path.dirname(__spec__.loader.path)


def configure():
    "configure directories to load modules from."
    name = Mods.package + ".modules" 
    dirs(name, os.path.join(Mods.path, "modules"))
    dirs("modules", moddir())
    if "m" in Config.opts:
        dirs("mods", "mods")


def dirs(name: str, path):
    "add module directory."
    Mods.dirs[name] = path


def importer(name, pth=""):
    "import module by path."
    if pth and os.path.exists(pth):
        spec = importlib.util.spec_from_file_location(name, pth)
    else:
        spec = importlib.util.find_spec(name)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    if not mod:
        return None
    Mods.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def mod(name):
    "import module by name." 
    if name in spl(Config.ignore):
        return None
    if name in Mods.modules:
        return Mods.modules[name]
    mname = ""
    pth = ""
    for packname, path in Mods.dirs.items():
        modpath = os.path.join(path, name + ".py")
        if os.path.exists(modpath):
            pth = modpath
            mname = f"{packname}.{name}"
            break
    return importer(mname, pth)


def mods(names):
    "list of named modules."
    return [
        mod(x) for x in sorted(spl(names))
        if x not in spl(Config.ignore)
        or x in spl(Config.sets.init)
    ]


def modules():
    "comma seperated list of available modules."
    mods = []
    for name, path in Mods.dirs.items():
        if name in spl(Config.ignore):
            continue
        if not os.path.exists(path):
            continue
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__") and x not in spl(Config.ignore)
        ])
    return ",".join(sorted(mods))


def __dir__():
    return (
        'Mods',
        'configure',
        'dirs',
        'importer',
        'mod',
        'modules'
    )
