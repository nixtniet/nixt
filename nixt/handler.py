# This file is placed in the Public Domain.


import queue
import threading


from .brokers import Broker
from .threads import launch


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()

    def callback(self, event):
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = launch(func, event, name=name)

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

    def register(self, kind, callback):
        self.cbs[kind] = callback

    def start(self):
        launch(self.loop)

    def stop(self):
        self.queue.put(None)


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock = threading.RLock()
        self.oqueue = queue.Queue()
        self.silent = True
        Broker.add(self)

    def announce(self, text):
        if not self.silent:
            self.raw(text)

    def display(self, event):
        with self.olock:
            for tme in sorted(event.result):
                self.dosay(
                           event.channel,
                           event.result[tme]
                          )

    def dosay(self, channel, text):
        self.say(channel, text)

    def raw(self, text):
        raise NotImplementedError("raw")

    def say(self, channel, text):
        self.raw(text)

    def wait(self):
        self.oqueue.join()


def __dir__():
    return (
        'Client',
        'Handler'
   )
