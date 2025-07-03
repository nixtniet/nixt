# This file is placed in the Public Domain.


"event handler"


import queue
import threading
import time
import _thread


from .objects import Object
from .threads import later, launch, name


class Handler:

    def __init__(self):
        self.lock  = _thread.allocate_lock()
        self.cbs     = {}
        self.queue   = queue.Queue()
        self.ready   = threading.Event()
        self.stopped = threading.Event()
        self.threshold = 50

    def available(self, evt):
        return evt.type in self.cbs

    def callback(self, event):
        func = self.cbs.get(event.type, None)
        event._thr = launch(func, event, daemon=True)

    def loop(self):
        while not self.stopped.is_set():
            with self.lock:
                event = self.poll()
                if event is None:
                    break
                if not self.available(event):
                    continue
                event.orig = repr(self)
                self.callback(event)
        self.ready.set()

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put(evt)

    def register(self, typ, cbs):
        self.cbs[typ] = cbs

    def start(self):
        self.stopped.clear()
        launch(self.loop)

    def stop(self):
        self.stopped.set()
        self.queue.put(None)
        self.ready.wait()

    def wait(self):
        self.queue.join()


class Event(Object):

    def __init__(self):
        Object.__init__(self)
        self._thr    = None
        self.channel = ""
        self.ctime   = time.time()
        self.orig    = ""
        self.rest    = ""
        self.result  = {}
        self.type    = "event"
        self.txt     = ""

    def done(self):
        self.reply("ok")

    def reply(self, txt):
        self.result[time.time()] = txt

    def wait(self, timeout=None):
        if self._thr:
            self._thr.join()


def __dir__():
    return (
        'Event',
        'Handler'
    )
