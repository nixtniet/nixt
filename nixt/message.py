# This file is placed in the Public Domain.


"only message"


import threading
import time


from .brokers import Broker
from .objects import Default


class Message(Default):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self.result = {}
        self.thr = None
        self.args = []
        self.index = 0
        self.kind = "event"
        self.orig = ""

    def display(evt):
        bot = Broker.get(evt.orig)
        bot.display(evt)
        
    def ready(self):
        self._ready.set()

    def reply(self, text):
        self.result[time.time()] = text

    def wait(self, timeout=0.0):
        if self.thr:
            self.thr.join(timeout)
        self._ready.wait(timeout or None)


def __dir__():
    return (
        'Message',
    )
