# This file is placed in the Public Domain.


"client"


from .engine import Engine
from .fleet  import Fleet


class Client(Engine):

    def __init__(self):
        Engine.__init__(self)
        Fleet.add(self)

    def announce(self, txt) -> None:
        pass

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None:
        self.raw(txt)


def __dir__():
    return (
        'Client',
    )
