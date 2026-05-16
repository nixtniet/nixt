# This file is placed in the Public Domain.


"clients"


import logging
import queue
import threading
import _thread


from .brokers import Broker
from .command import Commands
from .handler import Handler
from .message import Message
from .threads import Thread


class Client(Handler):

    def __init__(self):
        super().__init__()
        self.olock = threading.RLock()
        self.silent = True
        Broker.add(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for txt in event.result:
                self.dosay(event.channel, txt)

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def raw(self, text):
        "raw output."

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)


class Poller(Client):

    def loop(self):
        "polling loop."
        while not self.stopped.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            event.orig = repr(self)
            self.callback(event)
        self.done.set()

    def poll(self):
        return self.queue.get()


class Waiter(Client):

    def loop(self):
        "polling loop."
        while not self.stopped.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            event.orig = repr(self)
            self.callback(event)
            event.wait()
        self.done.set()


class Console(Waiter):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def poll(self):
        "return event."
        evt = Message()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        return evt


class Buffered(Poller):

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()
        self.ostopped = threading.Event()

    def output(self):
        "output loop."
        while not self.ostopped.is_set():
            try:
                event = self.oqueue.get()
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self, daemon=False):
        "start output loop."
        super().start(daemon=daemon)
        self.ostopped.clear()
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        self.ostopped.set()
        self.oqueue.put(None)
        super().stop()

    def wait(self):
        "wait for output to finish."
        try:
            super().wait()
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Buffered',
        'Client',
        'Console',
        'Poller',
        'Waiter'
    )
