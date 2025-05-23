# This file is placed in the Public Domain.


from queue     import Queue
from threading import Thread as IThread
from threading import Event, Timer
from typing    import Any, Callable, Dict, List


STARTTIME: float


class Errors:

    name: str
    errors: List


class Thread(IThread):

    def __init__(self, func: Callable, thrname: str, *args, daemon: bool=True, **kwargs):
        name: str
        queue:  Queue
        result: Any
        starttime: float
        stopped: Event

    def __iter__(self): ...
    def __next__(self): ...
    def run(self): ...
    def join(self, timeout=None): ...


class Timy(Timer):

    def __init__(self, *args: list[Any], **kwargs: Dict[str, Any]):
        state: Dict[str, Any]
        starttime: float


class Timed:

    def __init__(self, sleep: float, func: Callable, *args: list[Any], thrname: str = "", **kwargs: Dict[str, Any]):
        name:   str
        target: float
        timer:  Timer

    def run(self): ...
    def start(self): ...
    def stop(self): ...


class Repeater(Timed):

    def run(self) -> None: ...


def full(exc: Exception) -> str: ...
def later(exc: Exception) -> None: ...
def launch(func: Callable, *args, **kwargs) -> Thread: ...
def line(exc: Exception) -> str: ...
def name(obj: Any) -> str: ...
