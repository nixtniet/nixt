# This file is placed in the Public Domain.


"watching files"


import os
import threading
import time


from .threads import Thread


b = os.path.basename
e = os.path.exists


class Watcher:

    running = threading.Event()
    sleep = 1.0
    cbs = {}
    times = {}

    @classmethod
    def add(cls, path, callback):
        "add callback"
        if not os.path.exists(path):
            return
        cls.cbs[path] = callback
        
    @classmethod
    def callback(cls, path):
        "run callback."
        cls.cbs[path]()

    @classmethod
    def init(cls, times={}):
        "read timestamps."
        for path in cls.cbs:
            if not e(path):
                continue
            cls.times[path] = times.get(path, os.stat(path).st_mtime)
            
    @classmethod
    def loop(cls):
        "loop select."
        while cls.running.isSet():
            for path in cls.cbs:
                if not e(path):
                    continue
                mtime = os.stat(path).st_mtime
                if mtime > cls.times[path]:
                    cls.callback(path)
                cls.times[path] = mtime
            time.sleep(cls.sleep)

    @classmethod
    def start(cls, times={}):
        "start watcher"
        if cls.running.isSet():
            return
        cls.running.set()
        cls.init(times)
        Thread.launch(cls.loop, name="Watcher.loop")

    @classmethod
    def stop(cls):
        "stop watcher."
        cls.running.clear()


def __dir__():
    return (
        'Watcher',
    )
