# This file is placed in the Public Domain.


"an object for a string"


from .brokers import Broker
from .default import Event, RLock
from .handler import Handler
from .message import Message


class Display:

    "unit of display"

    block: Event = Event()
    last: str = ""

    def __init__(self):
        self.olock: RLock = RLock()
        self.silent: bool = False
        Broker.add(self)

    def announce(self, text: str) -> None:
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, msg: Message) -> None:
        "display msg results."
        with self.olock:
            for txt in msg.result:
                if self.block.is_set():
                    return
                self.dosay(msg.channel, txt)
                del txt
        del msg

    def dosay(self, channel: str, text: str) -> None:
        "say called by display."
        self.say(channel, text)

    def raw(self, text: str) -> None:
        "raw output."
        raise NotImplementedError

    def say(self, channel: str, text: str) -> None:
        "say text in channel."
        self.last = channel
        self.raw(text)


class Screen(Handler, Display):

    "display wit coupled handler."

    def __init__(self):
        Handler.__init__(self)
        Display.__init__(self)

    def raw(self, text: str) -> None:
        "raw output."
        raise NotImplementedError


def __dir__():
    return (
        'Display',
        'Screen'
    )
