# This file is placed in the Public Domain.


"event"


import threading
import time


from typing import Any, Iterator


from .object import Default


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time()
        self.orig   = ""
        self.result = {}
        self.type   = "event"
        self.txt    = ""

    def done(self) -> None:
        self.reply("ok")

    def ready(self) -> None:
        self._ready.set()

    def reply(self, txt: str) -> None:
        self.result[time.time()] = txt

    def wait(self) -> None:
        self._ready.wait()
        if self._thr:
            self._thr.join()


def __dir__():
    return (
        'Event',
    )
