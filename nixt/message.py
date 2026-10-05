# This file is placed in the Public Domain.


"only the msg"


from .default import Event
from .objects import Data
from .threads import Thread
from .typings import List, Union


Args   = List[str]
Result = List[str]
Thr    = Union[Thread, None]


class Message(Data):

    "msg as an msg"

    def __init__(self):
        super().__init__()
        self._ready: Event = Event()
        self._thr: Thr = None
        self.args: Args = []
        self.cmd: str = ""
        self.index: int = 0
        self.kind: str = "msg"
        self.orig: str = ""
        self.rest: str = ""
        self.result: Result = []
        self.text: str = ""

    def iface(self, text: str) -> None:
        "show interface."
        self.reply(f"{self.cmd} {text}")

    def ok(self, text: str = "") -> None:
        "print ok response."
        self.reply(f"ok {text}".strip())

    def ready(self) -> None:
        "flag msg as ready."
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
