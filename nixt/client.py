# This file is placed in the Public Domain.


"clients"


import os


from .command import command
from .fleet   import Fleet
from .object  import Default
from .output  import Output
from .reactor import Reactor


class Config(Default):

    init    = ""
    name    = __file__.rsplit(os.sep, maxsplit=2)[-2]
    opts    = Default()
    version = 200


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)
        self.register("command", command)

    def announce(self, txt):
        pass

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None:
        self.raw(txt)


class Buffered(Client, Output):

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def start(self) -> None:
        Output.start(self)
        Client.start(self)

    def stop(self) -> None:
        Output.stop(self)
        Client.stop(self)

    def wait(self) -> None:
        Client.wait(self)
        Output.wait(self)


def __dir__():
    return (
        'Client',
        'Config'
    )
