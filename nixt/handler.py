# This file is placed in the Public Domain.


import queue
import threading


from .threads import launch


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()

    def callback(self, event):
        if event.kind not in self.cbs:
            return event.ready()
        func = self.cbs.get(event.kind)
        name = event.text and event.text.split()[0]
        event._thr = launch(func, event, name=name)

    def loop(self):
        while not self.stopped.isSet():
            event = self.poll()
            event.orig = repr(self)
            self.callback(event)

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put(event)

    def register(self, kind, callback):
        self.cbs[kind] = callback

    def start(self):
        self.stopped.clear()
        launch(self.loop)

    def stop(self):
        self.stopped.set()


def __dir__():
    return (
        'Handler',
    )
