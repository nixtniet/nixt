# This file is placed in the Public Domain.


"event handler"


import _thread


from .errors  import later
from .event   import Event
from .fleet   import Fleet
from .reactor import Reactor


class Handler(Reactor):

    def callback(self, evt) -> None:
        func = self.cbs.get(evt.type, None)
        if not func:
            evt.ready()
            return
        func(evt)


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
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
        'Handler'
    )
