# This file is placed in the Public Domain.


"module management"


import importlib.util
import os


from .command import scancmd
from .threads import launch
from .utility import spl


class Mods:

    dirs = {}


def adddir(name, path):
    Mods.dirs[name] = path


def addpkg(pkg):
    Mods.dirs[pkg.__name__] = pkg.__path__[0]


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
    spec.loader.exec_module(mod)
    return mod


def modules(ignore=""):
    "comma seperated list of available modules."
    mods = []
    for pkgname, path in Mods.dirs.items():
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and
            not x.startswith("__") and
            x[:-3] not in spl(ignore)
        ])
    return ",".join(sorted(mods))


def scanner(inits="", wait=False):
    "scan named modules for commands."
    mods = []
    thrs = []
    for pkgname, path in Mods.dirs.items():
        for fnm in os.listdir(path):
            if fnm.startswith("__"):
                continue
            if not fnm.endswith(".py"):
                continue
            name = fnm[:-3]
            modname = f"{pkgname}.{name}"
            mod = importer(modname, os.path.join(path, fnm))
            if not mod:
                continue
            scancmd(mod)
            mods.append(mod)
            if name not in spl(inits):
                continue
            if "init" not in dir(mod):
                continue
            thrs.append(launch(mod.init))
    if wait:
        for thr in thrs:
            thr.join()
    return mods


def __dir__():
    return (
        'Mods',
        'adddir',
        'addpkg',
        'importer',
        'modules',
        'scanner'
    )
