# This file is placed in the Public Domain.


"handler"


import queue
import threading
import time


from .command import Commands


class Handler:

    def __init__(self):
        self.iqueue = queue.Queue()
        self.olock = threading.RLock()
        self.silent = True
        self.stopped = threading.Event()

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for tme in event.result:
                self.dosay(event.channel, event.result.get(tme))

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def loop(self):
        "input loop."
        while True:
            event = self.poll()
            if not event or self.stopped.is_set():
                break
            event.orig = repr(self)
            Commands.command(event)
            time.sleep(0.001)

    def poll(self):
        "return event."
        return self.iqueue.get()

    def put(self, event):
        self.iqueue.put(event)

    def raw(self, text):
        "raw output."

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)

    def start(self):
        "start handler."
        self.loop()


def __dir__():
    return (
        "Handler",
    )
