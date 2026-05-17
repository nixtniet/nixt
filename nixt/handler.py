# This file is placed in the Public Domain.


"event handling"


import logging
import queue
import threading
import _thread


from .brokers import Broker
from .command import Commands
from .objects import Base
from .threads import Thread


class Event(Base):

    def __init__(self):
        super().__init__()
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
        Broker.display(self)

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
        self.istopped = threading.Event()
        self.idone = threading.Event()
        Broker.add(self)

    def handle(self, event):
        "handle evemt."
        raise NotImplementedError

    def input(self):
        "input loop."
        while not self.istopped.is_set():
            event = self.poll()
            if event is None:
                break
            self.handle(event)
        self.idone.set()

    def poll(self):
        "return event."
        raise NotImplementedError

    def start(self, daemon=True):
        "start event handler loop."
        self.idone.clear()
        self.istopped.clear()
        Thread.launch(self.input, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        self.istopped.set()
        self.idone.wait()


def __dir__():
    return (
        'Event',
        'Handler'
    )
