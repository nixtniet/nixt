# This file is placed in the Public Domain.


from .objects import Default
from .package import Mods
from .workdir import Workdir


class Config(Default):

    name = "nixt"
    version = 440


def configure(name, version):
    Config.name = name
    Config.version = version
    Workdir.init(name)
    Mods.init(f"{name}.modules", local=True)


def __dir__():
    return (
        'Config',
    )
