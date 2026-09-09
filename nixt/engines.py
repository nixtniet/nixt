# This file is placed in the Public Domain.


"handling"


import queue
import threading


from .looping import Loop
from .threads import Thread


class Engine(Loop):

    def __init__(self):
        Loop.__init__(self)
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.done = threading.Event()

    def handle(self, event):
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = Thread.launch(func, event, name=name)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback


def __dir__():
    return (
        'Engine',
    )
