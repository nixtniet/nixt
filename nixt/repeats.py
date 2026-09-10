# This file is placed in the Public Domain.


"if it repeats it is important"


import threading
import time


from .threads import Thread


class Repeater:

    "repeat at interval"

    running = threading.Event()
    stopped = threading.Event()
    counter = 0
    sleeptime = 0.1
    todo = {}

    @classmethod
    def add(cls, sleep, func, *args, **kwargs):
        "add a repeater."
        sleep = str(sleep)
        if sleep not in cls.todo:
            cls.todo[sleep] = []
        cls.todo[sleep].append((func, args, kwargs))

    @classmethod
    def loop(cls):
        "repeater loop."
        while not cls.stopped.is_set():
            time.sleep(1.0)
            cls.counter += 1
            for sleep in cls.todo:
                slept = int(sleep)
                if cls.counter % slept != 0:
                    continue
                for func, args, kwargs in cls.todo[sleep]:
                    Thread.launch(func, *args, **kwargs)

    @classmethod
    def start(cls, daemon=True):
        "start callback loop."
        if not cls.stopped.is_set():
            Thread.launch(cls.loop, daemon=daemon, name="Repeater.loop")

    @classmethod
    def stop(cls):
        "stop loop"
        cls.stopped.set()
        
    @classmethod
    def wait(cls):
        "wait for loop to stop."


def __dir__():
    return (
        'Repeater',
    )
