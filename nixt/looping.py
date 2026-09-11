# This file is placed in the Public Domain.


"the big loop"


import queue
import threading
import _thread


from .threads import Thread


class Loop:

    "keep looping"

    def __init__(self):
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.done = threading.Event()

    def after(self, event):
        "called after callback."

    def handle(self, event):
        "handle event."

    def loop(self):
        "callback loop."
        while not self.stopped.is_set():
            self.poll()
            event = self.queue.get()
            if event is None:
                self.queue.task_done()
                break
            event.orig = repr(self)
            self.handle(event)
            self.after(event)
            self.queue.task_done()
        self.done.set()

    def poll(self):
        "create event and put it on the queue."

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def start(self, daemon=True):
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Thread.launch(self.loop, daemon=daemon)

    def stop(self):
        "stop xallback loop."
        self.stopped.set()
        self.queue.put(None)
        self.done.wait()

    def wait(self):
        "wait for all events to finish,"
        try:
            self.queue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def __dir__():
    return (
        'Loop',
    )
