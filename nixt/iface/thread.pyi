# This file is placed in the Public Domain.


"threading"


import queue
import time
import threading
import traceback
import _thread


from typing import Any, Callable


from threading import Event, Timer


STARTTIME = time.time()


class Errors:

    name: str
    errors: list


class Thread(threading.Thread):

    def __init__(self, func: Callable, thrname: str, *args, daemon: bool=True, **kwargs):
        name: str
        queue:  queue.Queue
        result: Any
        starttime: float
        stopped = Event

    def __iter__(self): ...
    def __next__(self): ...
    def run(self): ...
    def join(self, timeout=None): ...


class Timy(Timer):

    def __init__(self, *args, **kwargs):
        state: dict
        starttime: float


class Timed:

    def __init__(self, sleep, func, *args, thrname=None, **kwargs):
        args:   list[Any]
        func:   Callable
        kwargs: dict
        sleep:  float
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


def __dir__():
    return (
        'STARTTIME',
        'Errors',
        'Repeater',
        'Thread',
        'Timed',
        'full',
        'later',
        'launch',
        'line',
        'name'
    )
