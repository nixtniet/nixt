# This file is placed in the Public Domain.


from .configs import Config
from .package import Mods
from .workdir import Workdir


class Kernel:

    @staticmethod
    def configure(name, version):
        Config.name = name
        Config.version = version
        Workdir.init(name)
        Mods.init(f"{name}.modules", local=True)


def __dir__():
    return (
        'Kernel',
   )
