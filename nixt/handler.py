# This file is placed in the Public Domain.


"event handler"


import queue
import threading


from .threads import Thread


class Handler:

    def __init__(self):
        self.idone = threading.Event()
        self.iqueue = queue.Queue()
        self.istopped = threading.Event()

    def handle(self, event):
        "handle event."
        raise NotImplementedError

    def poller(self):
        "polling loop."
        while not self.istopped.is_set():
            event = self.poll()
            if event is None:
                break
            event.orig = repr(self)
            self.handle(event)
        self.idone.set()

    def poll(self):
        "return event."
        return self.iqueue.get()

    def put(self, event):
        "put event on queue."
        self.iqueue.put(event)

    def start(self, daemon=True):
        "start polling loop."
        self.idone.clear()
        self.istopped.clear()
        Thread.launch(self.poller, daemon=daemon)

    def stop(self):
        "stop polling loop."
        self.istopped.set()
        self.idone.wait()


def __dir__():
    return (
        'Handler',
    )
