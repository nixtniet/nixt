# This file is placed in the Public Domain.


"handling"


from typing import Callable


from .looping import Loop
from .message import Message
from .threads import Thread



class Engine(Loop):

    "run callbacks"

    def __init__(self):
        Loop.__init__(self)
        self.cbs = {}

    def handle(self, event: Message) -> None:
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = Thread.launch(func, event, name=name)

    def register(self, kind: str, callback: Callable) -> None:
        "register callback."
        self.cbs[kind] = callback


def __dir__():
    return (
        'Engine',
    )
