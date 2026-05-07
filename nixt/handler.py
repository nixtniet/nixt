# This file is placed in the Public Domain.


"event handling"


import logging
import queue
import threading
import _thread


from .brokers import Broker
from .command import Commands
from .objects import Object
from .threads import Thread


class Event(Object):

    def __init__(self):
        Object.__init__(self)
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.channel = ""
        self.cmd = ""
        self.index = 0
        self.kind = "event"
        self.orig = ""
        self.result = []
        self.text = ""

    def display(self):
        "print results."
        bot = Broker.get(self.orig)
        if bot:
            bot.display(self)

    def ok(self, txt=""):
        "print ok response."
        self.reply(f"ok {txt}".strip())

    def ready(self):
        "flag message as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result.append(text)

    def wait(self, timeout=0.0):
        "wait for completion."
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout or None)


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
        event._thr = Thread.launch(func, event, name=name)

    def loop(self):
        "event loop."
        while self.running.is_set():
            event = self.queue.get()
            if event is None:
                self.queue.task_done()
                break
            event.orig = repr(self)
            self.callback(event)
            self.queue.task_done()

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self, daemon=True):
        "start event handler loop."
        self.running.set()
        Thread.launch(self.loop, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        self.running.clear()
        self.queue.put(None)

    def wait(self):
        self.queue.join()


def __dir__():
    return (
        'Event',
        'Handler'
    )
