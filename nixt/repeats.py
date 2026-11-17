# This file is placed in the Public Domain.


"if it repeats it is important"


import time


from .tasking import Task
from .utility import Event


class Repeater:

    "repeat at interval"

    running = Event()
    stopped = Event()
    counter = 0
    sleeptime = 0.1
    todo = {}

    @classmethod
    def add(cls, sleeptime, func, *args, **kwargs):
        "add a repeater."
        slp = str(sleeptime)
        if slp not in cls.todo:
            cls.todo[slp] = []
        cls.todo[slp].append((func, args, kwargs))

    @classmethod
    def loop(cls):
        "repeater loop."
        while cls.running.is_set():
            time.sleep(1.0)
            cls.counter += 1
            for sleeptime, arguments in cls.todo.items():
                slept = int(sleeptime)
                if cls.counter % slept != 0:
                    continue
                for func, args, kwargs in arguments:
                    Task.begin(func, *args, **kwargs)
        cls.stopped.set()

    @classmethod
    def start(cls):
        "start callback loop."
        if cls.running.is_set():
            return
        cls.stopped.clear()
        cls.running.set()
        Task.begin(cls.loop, name="Repeater")

    @classmethod
    def stop(cls):
        "stop loop."
        cls.running.clear()

    @classmethod
    def wait(cls):
        "wait for loop to stop."
        cls.stopped.wait()


def __dir__():
    return (
        'Repeater',
    )
