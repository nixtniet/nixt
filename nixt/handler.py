# This file is placed in the Public Domain.


"callback engine"


import queue
import threading
import time


from .objects import Data
from .threads import Thread


class Broker:

    objects = {}

    @classmethod
    def add(cls, obj):
        "add object to the broker, key is repr(obj)."
        cls.objects[repr(obj)] = obj

    @classmethod
    def announce(cls, txt):
        "announce text on all objects with an announce method."
        for obj in cls.objs("announce"):
            obj.announce(txt)

    @classmethod
    def get(cls, origin):
        "object by repr(obj)."
        return cls.objects.get(origin)

    @classmethod
    def has(cls, obj):
        "whether the Broker has object."
        return repr(obj) in cls.objects

    @classmethod
    def like(cls, txt):
        "all keys with a substring in their key."
        for orig in cls.objects:
            if txt in orig.split()[0]:
                yield orig, cls.get(orig)

    @classmethod
    def objs(cls, attr):
        "objects with a certain attribute."
        for obj in cls.objects.values():
            if attr in dir(obj):
                yield obj


class Event(Data):

    def __init__(self):
        Data.__init__(self)
        self._ready = threading.Event()
        self._thr = None
        self.result = {}
        self.args = []
        self.index = 0
        self.orig = ""
        self.kind = "event"

    def display(self):
        bot = Broker.get(self.orig)
        if bot:
            bot.display(self)

    def ok(self, txt=""):
        self.reply(f"ok {txt}".strip())

    def ready(self):
        "flag message as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result[time.time()] = text

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

    def start(self):
        "start event handler loop."
        self.running.set()
        Thread.launch(self.loop)

    def stop(self):
        "stop event handler loop."
        self.running.clear()
        self.queue.put(None)


def __dir__():
    return (
        'Event',
        'Handler'
    )
