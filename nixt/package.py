# This file is placed in the Public Domain.


"module management"


import os


from .configs import Config
from .utility import spl


class Mods:

    package = __spec__.parent or ""
    path = os.path.dirname(__spec__.loader.path)


def mod(pkg, name):
    if pkg is None:
        return None
    return getattr(pkg, name, None)


def mods(pkg, names=""):
    if pkg is None:
        return []
    return [
            mod(pkg, x) for x in sorted(spl(names or modules(pkg)))
            if x not in spl(Config.ignore)
            or x in spl(Config.sets.init)]


def modules(pkg, ignore=""):
    if pkg is None:
        return ""
    modz = []
    path = pkg.__path__[0]
    modz.extend([
        x[:-3] for x in os.listdir(path)
        if x.endswith(".py") and not x.startswith("__")
    ])
    return ",".join(sorted(modz)).strip()


def __dir__():
    return (
        'Mods',
        'mod',
        'mods',
        'modules'
    )
