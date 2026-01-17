# This file is placed in the Public Domain.


"only messages"


import threading
import time


from .objects import Default


class Message(Default):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self._thr = None
        self.result = {}
        self.args = []
        self.index = 0
        self.kind = "event"
        self.orig = ""

    def ready(self):
        "flag message as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result[time.time()] = text

    def wait(self, timeout=0.0):
        "wait for completion."
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout)


def __dir__():
    return (
        'Message',
    )
