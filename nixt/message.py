# This file is placed in the Public Domain.


"only the msg"


from .default import Event
from .objects import Data
from .tasking import Worker
from .typings import List, Union


class Message(Data):

    "msg as an msg"

    def __init__(self):
        super().__init__()
        self.__ready__: Event = Event()
        self.__thr__: Union[Worker ,None] = None
        self.args: List[str] = []
        self.cmd: str = ""
        self.index: int = 0
        self.kind: str = "msg"
        self.orig: str = ""
        self.rest: str = ""
        self.result: List[str] = []
        self.text: str = ""

    def __iter__(self):
        return iter([x for x in self.__dict__ if not x.startswith("_")])

    def iface(self, text):
        "show interface."
        self.reply(f"{self.cmd} {text}")

    def ok(self, text=""):
        "print ok response."
        self.reply(f"ok {text}".strip())

    def ready(self):
        "flag msg as ready."
        self.__ready__.set()

    def reply(self, text):
        "add text to result."
        self.result.append(text)

    def wait(self, timeout=0.0):
        "wait for completion."
        self.__ready__.wait(timeout or None)
        if self.__thr__:
            self.__thr__.join(timeout or None)


def __dir__():
    return (
        'Message',
    )
