# This file is placed in the Public Domain.


"callback engine"


from .looping import Loop
from .message import Message
from .threads import Thread
from .typings import Callable, Dict


Callables = Dict[str, Callable]


class Engine(Loop):

    "run callbacks"

    def __init__(self):
        super().__init__()
        self.cbs: Callables = {}

    def handle(self, msg: Message) -> None:
        "run callback function with msg."
        func = self.cbs.get(msg.kind, None)
        if not func:
            msg.ready()
            return
        name = msg.text and msg.text.split()[0]
        msg._thr = Thread.launch(func, msg, name=name)

    def register(self, kind: str, callback: Callable) -> None:
        "register callback."
        self.cbs[kind] = callback


def __dir__():
    return (
        'Engine',
    )
