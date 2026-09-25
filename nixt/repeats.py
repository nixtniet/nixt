# This file is placed in the Public Domain.


"if it repeats it is important"


import time


from collections.abc import Callable
from threading       import Event
from typing          import Any, ClassVar, Dict, List


from .threads import Thread


class Repeater:

    "repeat at interval"

    running: ClassVar[Event] = Event()
    stopped: ClassVar[Event] = Event()
    counter: ClassVar[int] = 0
    sleeptime: ClassVar[float] = 0.1
    todo: ClassVar[Dict[str, List[Any]]] = {}

    @classmethod
    def add(cls, sleep: float, func: Callable, *args: Any, **kwargs: Dict[str, Any]) -> None:
        "add a repeater."
        slp = str(sleep)
        if slp not in cls.todo:
            cls.todo[slp] = []
        cls.todo[slp].append((func, args, kwargs))

    @classmethod
    def loop(cls) -> None:
        "repeater loop."
        while not cls.stopped.is_set():
            time.sleep(1.0)
            cls.counter += 1
            for sleep, arguments in cls.todo.items():
                slept = int(sleep)
                if cls.counter % slept != 0:
                    continue
                for func, args, kwargs in arguments:
                    Thread.launch(func, *args, **kwargs)

    @classmethod
    def start(cls, daemon: bool = True) -> None:
        "start callback loop."
        if not cls.stopped.is_set():
            Thread.launch(cls.loop, daemon=daemon, name="Repeater.loop")

    @classmethod
    def stop(cls) -> None:
        "stop loop."
        cls.stopped.set()

    @classmethod
    def wait(cls) -> None:
        "wait for loop to stop."


def __dir__():
    return (
        'Repeater',
    )
