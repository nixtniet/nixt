# This file is placed in the Public Domain.


"event handler"


import queue
import threading


from .brokers import Broker
from .objects import Base
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


class Message(Base):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.channel = ""
        self.cmd = ""
        self.mod = ""
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

    def iface(self, txt):
        "show interface."
        txt = f"{self.cmd} {txt}"
        if txt.startswith("."):
            txt = txt[1:]
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
        'Handler',
        'Message'
    )
