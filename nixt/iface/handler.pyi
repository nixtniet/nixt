# This file is placed in the Public Domain.


"event handler"


import queue
import threading
import _thread


from typing import Callable


from .event  import Event
from .thread import later, launch, name


lock = threading.RLock()


class Handler:

    def __init__(self) -> None:
        cbs:     dict
        queue:   queue.Queue
        ready:   threading.Event()
        stopped: threading.Event()

    def callback(self, evt: Event) -> None: ...

    def loop(self): ...
    def poll(self): ...
    def put(self, evt: Event): ...
    def register(self, typ: str, cbs: Callable): ...
    def start(self): ...
    def stop(self): ...
    def wait(self): ...


def __dir__():
    return (
        'Handler',
    )
