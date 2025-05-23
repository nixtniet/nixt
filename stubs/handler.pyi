# This file is placed in the Public Domain.


import threading


from queue     import Queue
from threading import Event, RLock
from typing    import Callable


from .event  import Event as IEvent
from .thread import later, launch, name


lock = RLock()


class Handler:

    def __init__(self) -> None:
        cbs:     dict
        queue:   Queue
        ready:   Event
        stopped: Event

    def callback(self, evt: IEvent) -> None: ...
    def loop(self): ...
    def poll(self): ...
    def put(self, evt: IEvent): ...
    def register(self, typ: str, cbs: Callable): ...
    def start(self): ...
    def stop(self): ...
    def wait(self): ...
