# This file is placed in the Public Domain.


"only the message"


import threading


from .brokers import Broker
from .objects import Object


class Message(Object):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.index = 0
        self.kind = "message"
        self.result = []

    def __getattr__(self, key):
        if key in dir(self):
            return self.__getattribute__(self, key)
        return ""

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
        'Message',
    )
