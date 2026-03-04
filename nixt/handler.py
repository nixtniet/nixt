# This file is placed in the Public Domain.


"callback engine"


import logging
import queue
import threading
import time
import _thread


from nixt.threads import exceptions, launch


class Event:

    """Event"""

    def __init__(self):
        self.isready = threading.Event()
        self.thr = None
        self.result = {}
        self.args = []
        self.index = 0
        self.kind = "event"
        self.orig = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __str__(self):
        return str(self.__dict__)

    def ready(self):
        "flag message as ready."
        self.isready.set()

    def reply(self, text):
        "add text to result."
        self.result[time.time()] = text

    def wait(self, timeout=0.0):
        "wait for completion."
        if self.thr:
            self.thr.join(timeout)
        self.isready.wait(timeout or None)


class Handler:

    """Handler"""

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
        event.thr = launch(func, event, name=name)

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
        'Event',
        'Handler'
    )
