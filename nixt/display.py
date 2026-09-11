# This file is placed in the Public Domain.


"an object for a string"


import threading


from .brokers import Broker
from .engines import Engine


class Display:

    "unit of display"

    block = threading.Event()

    def __init__(self):
        self.olock = threading.RLock()
        self.silent = False

    def announce(self, text):
        "announce text to all channels"
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results"
        with self.olock:
            for txt in event.result:
                if self.block.is_set():
                    return
                self.dosay(event.channel, txt)
                del txt
        del event

    def dosay(self, channel, text):
        "say called by display"
        self.say(channel, text)

    def raw(self, text):
        "raw output"
        raise NotImplementedError

    def say(self, channel, text): # pylint: disable=W0613
        "say text in channel"
        self.raw(text)


class Screen(Engine, Display):

    "display wit coupled handler"

    def __init__(self):
        Engine.__init__(self)
        Display.__init__(self)
        Broker.add(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


def __dir__():
    return (
        'Display',
        'Screen'
    )
