# This file is placed in the Public Domain.


"watching files"


import os
import time


from .default import Event
from .threads import Threading
from .typings import Callable, ClassVar, Dict, Union


Callables = Dict[str, Callable]
Floats    = Dict[str, float]


e = os.path.exists


class Watcher:

    "watch files"

    cbs: ClassVar[Callables] = {}
    sleep: float = 1.0
    stopped: Event = Event()
    times: ClassVar[Floats] = {}

    @classmethod
    def add(cls, path: str, callback: Callable):
        "add callback"
        if not e(path):
            return
        cls.cbs[path] = callback

    @classmethod
    def init(cls, times: Union[Dict[str,int], None] = None):
        "read timestamps."
        if times is None:
            times= {}
        for path in cls.cbs:
            if not e(path):
                continue
            cls.times[path] = times.get(path, os.stat(path).st_mtime)

    @classmethod
    def loop(cls):
        "loop select."
        while not cls.stopped.is_set():
            for path, callback in cls.cbs.items():
                if not e(path):
                    continue
                mtime = os.stat(path).st_mtime
                if mtime > cls.times[path]:
                    callback()
                cls.times[path] = mtime
            time.sleep(cls.sleep)

    @classmethod
    def start(cls, daemon: bool = True):
        "start callback loop."
        if not cls.stopped.is_set():
            return
        Threading.launch(cls.loop, daemon=daemon)

    @classmethod
    def stop(cls):
        "stop xallback loop."
        cls.stopped.set()


def __dir__():
    return (
        'Watcher',
    )
