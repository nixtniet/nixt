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

    def iface(self, txt) -> None:
        "show interface."
        txt = f"{self.cmd} {txt}"
        self.reply(txt)

    def ok(self, txt="") -> None:
        "print ok response."
        self.reply(f"ok {txt}".strip())

    def ready(self) -> None:
        "flag message as ready."
        self._ready.set()

    def reply(self, text) -> None:
        "add text to result."
        self.result.append(text)

    def wait(self, timeout=0.0) -> None:
        "wait for completion."
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout or None)


def __dir__():
    return (
        'Message',
    )
