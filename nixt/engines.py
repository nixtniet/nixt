# This file is placed in the Public Domain.


"callback engine"


import queue
import threading
import _thread


from .objects import Data
from .threads import Thread


class Engine:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.done = threading.Event()

    def after(self, event):
        "called after callback."

    def callback(self, event):
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = Thread.launch(func, event, name=name)

    def loop(self):
        "callback loop."
        while not self.stopped.is_set():
            self.poll()
            event = self.queue.get()
            if event is None:
                self.queue.task_done()
                break
            event.orig = repr(self)
            self.callback(event)
            self.after(event)
            self.queue.task_done()
        self.done.set()

    def poll(self):
        "create event and put it on the queue."

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

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


class Message(Data):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.index = 0
        self.kind = "message"
        self.result = []

    def iface(self, txt):
        "show interface."
        txt = f"{self.cmd} {txt}"
        self.reply(txt)

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


def __dir__():
    return (
        'Engine',
        'Message'
    )
