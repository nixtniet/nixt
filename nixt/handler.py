# This file is placed in the Public Domain.


"event handler."


import queue
import threading


from .brokers import Broker
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
        self.idone = threading.Event()
        self.iqueue = queue.Queue()
        self.istopped = threading.Event()

    def handle(self, event):
        "handle event."
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
        return self.iqueue.get()

    def put(self, event):
        "put event on queue."
        self.iqueue.put(event)

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
