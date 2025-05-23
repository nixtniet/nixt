# This file is placed in the Public Domain.


from threading import Event as IEvent
from typing    import Any, Iterator


from .thread import Thread


class Event:

    def __init__(self) -> None:
        _ready: IEvent
        _thr:   Thread
        ctime:  float
        orig:   str
        result: dict
        type:   str
        txt:    str

    def __contains__(self, key: str) -> list[str]: ...
    def __getattr__(self, key: str) -> Any: ...
    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    def done(self) -> None: ...
    def ready(self) -> None: ...
    def reply(self, txt: str) -> None: ...
    def wait(self) -> None: ...
