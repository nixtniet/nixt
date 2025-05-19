# This file is placed in the Public Domain.


"threading"


import time


from threading import Event, Timer
from threading import Thread as IThread


STARTTIME = time.time()


class Errors:

    name = __file__.rsplit("/", maxsplit=2)[-2]
    errors = []


class Thread(IThread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs): ...
    def __iter__(self): ...
    def __next__(self): ...
    def run(self) -> None: ...
    def join(self, timeout=None): ...


class Timy(Timer):

    def __init__(self, *args, **kwargs): ...


class Timed:

    def __init__(self, sleep, func, *args, thrname=None, **kwargs):
        self.args      = args
        self.func      = func
        self.kwargs    = kwargs
        self.sleep     = sleep
        self.name      = thrname or kwargs.get("name", name(func))
        self.target    = time.time() + self.sleep
        self.timer     = None

    def run(self) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...


class Repeater(Timed):

    def run(self) -> None: ...


def full(exc) -> str: ...
def later(exc) -> None: ...
def launch(func, *args, **kwargs) -> Thread: ...
def line(exc): ...
def name(obj) -> str: ...
