# This file is placed in the Public Domain.


"event handler"


import _thread


from .errors  import later
from .event   import Event
from .fleet   import Fleet
from .reactor import Reactor


class Handler(Reactor):

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                func = self.cbs.get(evt.type, None)
                if not func:
                    evt.ready()
                    return
                func(evt)
            except Exception as ex:
                later(ex)
                _thread.interrupt_main()
        self.ready.set()

    def poll(self) -> Event:
        return self.queue.get()


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
