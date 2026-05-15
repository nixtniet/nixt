# This file is placed in the Public Domain.


"event handling"


import queue
import threading


from .threads import Thread


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.done = threading.Event()

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
        while not self.stopped.is_set():
            event = self.queue.get()
            if event is None:
                print("end")
                self.queue.task_done()
                break
            event.orig = repr(self)
            self.callback(event)
            self.queue.task_done()
        print("yo!")
        self.done.set()

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self, daemon=True):
        "start event handler loop."
        self.done.clear()
        self.stopped.clear()
        Thread.launch(self.loop, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        self.stopped.set()
        print("put")
        self.queue.put(None)
        self.done.wait()

    def wait(self):
        "wait for all events to finish,"
        self.queue.join()


def __dir__():
    return (
        'Handler',
    )
