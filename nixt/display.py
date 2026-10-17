# This file is placed in the Public Domain.


"displaying messages"


from .brokers import Broker
from .default import Event, RLock
from .handler import Handler


class Display:

    "unit of display"

    block = Event()
    last = ""

    def __init__(self):
        self.olock: RLock = RLock()
        self.silent: bool = False
        Broker.add(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, msg):
        "display msg results."
        with self.olock:
            for txt in msg.result:
                if self.block.is_set():
                    return
                self.dosay(msg.channel, txt)
                del txt
        del msg

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def say(self, channel, text):
        "say text in channel."
        self.last = channel
        self.raw(text)


class Screen(Handler, Display):

    "display wit coupled handler."

    def __init__(self):
        Handler.__init__(self)
        Display.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


def __dir__():
    return (
        'Display',
        'Screen'
    )
