# This file is placed in the Public Domain.


"message handler"


from .looping import Loop
from .message import Message
from .tasking import Task
from .typings import Callable, Dict


Callbacks = Dict[str, Callable]


class Handler(Loop):

    "run callbacks"

    def __init__(self):
        super().__init__()
        self.cbs: Callbacks = {}

    def handle(self, msg: Message) -> None:
        "run callback function with msg."
        func = self.cbs.get(msg.kind, None)
        if not func:
            msg.ready()
            return
        name = msg.text and msg.text.split()[0]
        msg.__thr__ = Task.start(func, msg, name=name)

    def register(self, kind: str, callback: Callable) -> None:
        "register callback."
        self.cbs[kind] = callback


def __dir__():
    return (
        'Handler',
    )
