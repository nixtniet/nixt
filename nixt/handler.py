# This file is placed in the Public Domain.


import queue
import threading
import time


from .brokers import Broker
from .threads import launch


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()

    def callback(self, event):
        func = self.cbs.get(event.type, None)
        if func:
            name = event.text and event.text.split()[0]
            event._thr = launch(func, event, name=name)
        else:
            event.ready()

    def loop(self):
        while True:
            event = self.poll()
            if event is None:
                break
            event.orig = repr(self)
            self.callback(event)

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put(event)

    def register(self, type, callback):
        self.cbs[type] = callback

    def start(self):
        launch(self.loop)

    def stop(self):
        self.queue.put(None)


def __dir__():
    return (
        'Handler',
   )
