# This file is placed in the Public Domain.


import queue
import threading
import time


from .brokers import Broker


class Message:

    def __init__(self):
        self._ready = threading.Event()
        self._thr = None
        self.channel = ""
        self.ctime = time.time()
        self.orig = ""
        self.result = {}
        self.text = ""
        self.type = "event"

    def display(self):
        bot = Broker.get(self.orig)
        bot.display(self)

    def ready(self):
        self._ready.set()

    def reply(self, text):
        self.result[time.time()] = text

    def wait(self, timeout=None):
        self._ready.wait()
        if self._thr:
            self._thr.join(timeout)


def __dir__():
    return (
        'Message',
   )
