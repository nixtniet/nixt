# This file is placed in the Public Domain.


"event"


import time


from threading import Event as IEvent
from threading import Thread


from typing import Any, Dict, Iterator


from .object import Default


class Event(Default):

    def __init__(self) -> None:
        Default.__init__(self)
        self._ready: IEvent           = IEvent()
        self._thr:   Thread | None    = None
        self.ctime:  float            = time.time()
        self.orig:   str              = ""
        self.result: Dict[float, str] = {}
        self.type:   str              = "event"
        self.txt :   str              = ""

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
