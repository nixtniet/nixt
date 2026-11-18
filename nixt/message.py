 # This file is placed in the Public Domain.


"only the message"


from threading import Event


from .objects import Data


class Message(Data):

    "message as an event"

    def __init__(self):
        super().__init__()
        self._ready = Event()
        self._thr = None
        self.args = []
        self.cmd = ""
        self.index = 0
        self.kind = "message"
        self.orig = ""
        self.rest = ""
        self.result = []
        self.text = ""

    def __iter__(self):
        return iter(self.__dict__)

    def iface(self, text):
        "show interface."
        self.reply(f"{self.cmd} {text}")

    def isready(self):
        "see if message is processed."
        return self._ready.is_set()

    def ok(self, text=""):
        "print ok response."
        self.reply(f"ok {text}".strip())

    def parse(self):
        "parse message."
        try:
            self.cmd, *self.args = self.text.split()
            self.rest = " ".join(self.args)
            return True
        except ValueError:
            return False

    def ready(self):
        "flag msg as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result.append(text)

    def thread(self, thr):
        "set running thread."
        self._thr = thr

    def wait(self, timeout=0.0):
        "wait for completion."
        if self._thr:
            self._thr.join(timeout or None)
        self._ready.wait(timeout or None)


def __dir__():
    return (
        'Message',
    )
