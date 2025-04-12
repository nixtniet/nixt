# This file is placed in the Public Domain.


"clients"


from .fleet   import Fleet
from .object  import Object
from .output  import output
from .reactor import Reactor


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.state = Default()
        Fleet.add(self)

    def announce(self, txt) -> None:
        pass

    def raw(self, txt) -> None:
        output(txt.encode('utf-8', 'replace').decode("utf-8"))

    def say(self, channel, txt) -> None:
        self.raw(txt)


def __dir__():
    return (
        'Client',
        'Default'
    )
