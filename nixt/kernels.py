# This file is placed in the Public Domain.


from .configs import Config
from .workdir import Workdir
from .package import Mods


class Kernel:

    @staticmethod
    def boot(name, version):
        Config.name = name
        Config.version = version
        Workdir.init(Config.name)
        Mods.init(f"{Config.name}.modules", local=True)


def __dir__():
    return (
        'Kernel',
   )
