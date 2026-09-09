# This file is placed in the Public Domain.


"if it repeats it is important"


import threading
import time


from .looping import Loop
from .threads import Thread


class Repeater(Loop):

    counter = 0
    running = threading.Event()
    stopped = threading.Event()
    todo = {}

    def add(self, sleep, func, *args, **kwargs):
        "add a repeater."
        if not self.stopped.is_set():
            self.start()
        sleep = str(sleep)
        if sleep not in self.todo:
            self.todo[sleep] = []
        self.todo[sleep].append((func, args, kwargs))

    def loop(self):
        "repeater loop."
        while not self.stopped.is_set():
            time.sleep(1.0)
            self.counter += 1
            for sleep in self.todo:
                slept = float(sleep)
                if self.counter % slept != 0:
                    continue
                for func, args, kwargs in self.todo[sleep]:
                    Thread.launch(func, *args, **kwargs)

    def start(self, daemon=True):
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Thread.launch(self.loop, daemon=daemon, name="Repeater.loop")


def __dir__():
    return (
        'Repeater',
    )
