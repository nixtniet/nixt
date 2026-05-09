# This file is placed in the Public Domain.


"event handling"


import collections
import queue
import threading


from .threads import Thread


class Handler:

    def __init__(self):
        self.cbs = {}
        self.events = collections.deque()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.done = threading.Event()

    def callback(self, event):
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = Thread.launch(func, event, name=name)

    def loop(self):
        "event loop."
        while not self.stopped.is_set():
            event = self.queue.get()
            if event is None:
                break
            self.events.append(event)
            event.orig = repr(self)
            self.callback(event)
        self.done.set()

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self, daemon=True):
        "start event handler loop."
        self.done.clear()
        self.stopped.clear()
        Thread.launch(self.loop, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        self.stopped.set()
        self.queue.put(None)

    def wait(self):
        while True:
            try:
                # self.done.wait()
                event = self.events.pop()
                event.wait()
            except IndexError:
                break


def __dir__():
    return (
        'Handler'
    )
