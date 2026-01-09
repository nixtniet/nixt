# This file is placed in the Public Domain.


"module management"


import os


from .command import scancmd
from .threads import launch
from .utility import importer, spl


class Mods:

    dirs = {}
    modules = {}


def adddir(name, path):
    "add module directory."
    Mods.dirs[name] = path


def addpkg(*pkgs):
    "register package directory."
    for pkg in pkgs:
        adddir(pkg.__name__, pkg.__path__[0])


def getmod(name):
    "import module by name." 
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
    mod = importer(mname, pth)
    if mod:
        Mods.modules[name] = mod
    return mod


def init(names=None, wait=False):
    "run init function of modules."
    if names is None:
        names = modules()
    mods = []
    for name in spl(names):
        module = getmod(name)
        if not module:
            continue
        if "init" in dir(module):
            thr = launch(module.init)
            mods.append((module, thr))
    if wait:
        for module, thr in mods:
            thr.join()
    return mods


def mods(names):
    "list of named modules."
    return [getmod(x) for x in sorted(spl(names))]


def modules(ignore=""):
    "comma seperated list of available modules."
    mods = []
    for name, path in Mods.dirs.items():
        if not os.path.exists(path):
            continue
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and
            not x.startswith("__") and
            x[:-3] not in spl(ignore)
        ])
    return ",".join(sorted(mods))


def scanner(names):
    "scan named modules for commands."
    mods = []
    for name in spl(names):
        module = getmod(name)
        if not module:
            continue
        scancmd(module)
    return mods


def __dir__():
    return (
        'Mods',
        'adddir',
        'addpkg',
        'init',
        'mods',
        'modules',
        'scanner'
    )
