# This file is placed in the Public Domain.


"only the message"


import threading


from .objects import Data


class Message(Data):

    "message as an event"

    def __init__(self):
        Data.__init__(self)
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.cmd = ""
        self.index = 0
        self.kind = "message"
        self.orig = ""
        self.result = []
        self.text = ""

    def iface(self, text: str) -> None:
        "show interface."
        txt = f"{self.cmd} {text}"
        self.reply(text)

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
