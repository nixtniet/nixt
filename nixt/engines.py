# This file is placed in the Public Domain.


"handling"


from typing import Callable, Dict


from .looping import Loop
from .message import Message
from .threads import Thread


class Engine(Loop):

    "run callbacks"

    def __init__(self):
        Loop.__init__(self)
        self.cbs: Dict[str, Callable] = {}

    def handle(self, message: Message) -> None:
        "run callback function with message."
        func = self.cbs.get(message.kind, None)
        if not func:
            message.ready()
            return
        name = message.text and message.text.split()[0]
        message._thr = Thread.launch(func, message, name=name)

    def register(self, kind: str, callback: Callable) -> None:
        "register callback."
        self.cbs[kind] = callback


def __dir__():
    return (
        'Engine',
    )
