# This file is placed in the Public Domain.


"if it repeats it's important"


import threading
import time


from .objects import Base
from .threads import Thread


class Repeater:

    counter = 0
    fnm = ""
    running = threading.Event()
    stopped = threading.Event()
    todo = Base()

    @classmethod
    def add(cls, sleep, func, *args, **kwargs):
        "add a repeater."
        if not cls.running.is_set():
            cls.start()
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
                slept = float(sleep)
                if cls.counter % slept != 0:
                    continue
                for func, args, kwargs in cls.todo[sleep]:
                    Thread.launch(func, *args, **kwargs)

    @classmethod
    def start(cls):
        "start repeater loop."
        cls.running.set()
        cls.stopped.clear()
        Thread.launch(cls.loop, name="Repeater.loop")

    @classmethod
    def stop(cls):
        "stop repeater loop."
        cls.stopped.set()


def __dir__():
    return (
        'Repeater',
    )
