# This file is placed in the Public Domain.


"only the message"


from threading import Event
from typing    import Any, List, Union


from .objects import Data
from .threads import Thr


class Message(Data):

    "message as an event"

    def __init__(self):
        Data.__init__(self)
        self._ready: Event = Event()
        self._thr: Union[Thr, None] = None
        self.args: List[str] = []
        self.cmd: str = ""
        self.index: int = 0
        self.kind: str = "message"
        self.orig: str = ""
        self.rest: str = ""
        self.result: List[Any] = []
        self.text: str = ""

    def iface(self, text: str) -> None:
        "show interface."
        self.reply(f"{self.cmd} {text}")

    def ok(self, text: str = "") -> None:
        "print ok response."
        self.reply(f"ok {text}".strip())

    def ready(self) -> None:
        "flag message as ready."
        self._ready.set()

    def reply(self, text: str) -> None:
        "add text to result."
        self.result.append(text)

    def wait(self, timeout: float = 0.0) -> None:
        "wait for completion."
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout or None)


def __dir__():
    return (
        'Message',
    )
