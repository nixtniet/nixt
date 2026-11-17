# This file is placed in the Public Domain.


"watching files"


import os
import time


from .tasking import Task
from .utility import Event


class Watcher:

    "watch files"

    cbs = {}
    sleep  = 1.0
    running = Event()
    stopped = Event()
    times = {}

    @classmethod
    def add(cls, path, callback):
        "add callback."
        if not os.path.exists(path):
            return
        cls.cbs[path] = callback

    @classmethod
    def init(cls, times=None):
        "read timestamps."
        if times is None:
            times= {}
        for path in cls.cbs:
            if not os.path.exists(path):
                continue
            cls.times[path] = times.get(path, os.stat(path).st_mtime)

    @classmethod
    def loop(cls):
        "loop select."
        while cls.running.is_set():
            for path, callback in cls.cbs.items():
                if not os.path.exists(path):
                    continue
                mtime = os.stat(path).st_mtime
                if mtime > cls.times[path]:
                    callback()
                cls.times[path] = mtime
            time.sleep(cls.sleep)
        cls.stopped.set()

    @classmethod
    def start(cls, **kwargs):
        "start callback loop."
        if cls.running.is_set():
            return
        cls.running.set()
        kwargs["name"] = "Monitor"
        Task.begin(cls.loop, **kwargs)

    @classmethod
    def stop(cls):
        "stop xallback loop."
        cls.running.clear()

    @classmethod
    def wait(cls):
        "wait for monitor to stop."
        cls.stopped.wait()


def __dir__():
    return (
        'Watcher',
    )
