 # This file is placed in the Public Domain.


"only the message"


from .objects import Data
from .utility import Event


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

    def gets(self):
        "return selectors."
        return dict([x.split("==", maxsplit=1) for x in self.text.split() if "==" in x])

    def iface(self, text):
        "show interface."
        self.reply(f"{self.cmd} {text}")

    def indexes(self):
        return [int(x) for x in self.text.split() if x.startswith("-") and isinstance(x, int)]

    def isready(self):
        "see if message is processed."
        return self._ready.is_set()

    def ok(self, text=""):
        "print ok response."
        self.reply(f"ok {text}".strip())

    def ready(self):
        "flag msg as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result.append(text)

    def sets(self):
        "return setted attributes."
        return dict([x.split("=", maxsplit=1) for x in self.text.split() if "=" in x and not "==" in x])

    def thread(self, thr):
        "set running thread."
        self._thr = thr

    def wait(self, timeout=0.0):
        "wait for completion."
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout or None)


def __dir__():
    return (
        'Message',
    )
