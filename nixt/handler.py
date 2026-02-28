# This file is placed in the Public Domain.


"callback engine"


import logging
import queue
import threading
import _thread


from .brokers import Broker
from .threads import launch


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.running = threading.Event()
        
    def callback(self, event):
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = launch(func, event, name=name)

    def loop(self):
        "event loop."
        while self.running.is_set():
            event = self.queue.get()
            if not event:
                break
            event.orig = repr(self)
            self.callback(event)
        
    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self, daemon=True):
        "start event handler loop."
        self.running.set()
        launch(self.loop, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        self.running.clear()
        self.queue.put(None)




def __dir__():
    return (
        'Handler',
    )
