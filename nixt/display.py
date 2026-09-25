# This file is placed in the Public Domain.


"an object for a string"


import threading


from threading import Event, RLock


from .brokers import Broker
from .engines import Engine
from .message import Message


class Display:

    "unit of display"

    block: Event = Event()

    def __init__(self):
        self.olock: RLock = RLock()
        self.silent: bool = False

    def announce(self, text: str) -> None:
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event: Message) -> None:
        "display event results."
        with self.olock:
            for txt in event.result:
                if self.block.is_set():
                    return
                self.dosay(event.channel, txt)
                del txt
        del event

    def dosay(self, channel: str, text: str) -> None:
        "say called by display."
        self.say(channel, text)

    def raw(self, text: str) -> None:
        "raw output."
        raise NotImplementedError

    def say(self, channel: str, text: str) -> None:
        "say text in channel."
        self.raw(text)


class Screen(Engine, Display):

    "display wit coupled handler."

    def __init__(self):
        Engine.__init__(self)
        Display.__init__(self)
        Broker.add(self)

    def raw(self, text: str) -> None:
        "raw output."
        raise NotImplementedError


def __dir__():
    return (
        'Display',
        'Screen'
    )
