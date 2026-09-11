# This file is placed in the Public Domain.


"watching files"


import os
import threading
import time


from collections.abc import Callable
from typing import ClassVar


from .threads import Thread


e = os.path.exists


class Watcher:

    sleep = 1.0
    cbs: ClassVar[dict[str, Callable]] = {}
    stopped = threading.Event()
    times: ClassVar[dict[str, float]] = {}

    @classmethod
    def add(cls, path, callback):
        "add callback"
        if not e(path):
            return
        cls.cbs[path] = callback

    @classmethod
    def init(cls, times=None):
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
        while not cls.stopped.isSet():
            for path in cls.cbs:
                if not e(path):
                    continue
                mtime = os.stat(path).st_mtime
                if mtime > cls.times[path]:
                    cls.cbs[path]()
                cls.times[path] = mtime
            time.sleep(cls.sleep)

    @classmethod
    def start(cls, daemon=True):
        "start callback loop."
        if not cls.stopped.is_set():
            return
        Thread.launch(cls.loop, daemon=daemon)

    @classmethod
    def stop(cls):
        "stop xallback loop."
        cls.stopped.set()


def __dir__():
    return (
        'Watcher',
    )
