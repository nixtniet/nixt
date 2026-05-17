# This file is placed in the Public Domain.


"event handling"


import logging
import queue
import threading
import _thread


from .brokers import Broker
from .command import Commands
from .handler import Handler
from .message import Message
from .threads import Thread


class Input(Handler):

    def __init__(self):
        super().__init__()
        self.iqueue = queue.Queue()
        self.istopped = threading.Event()
        self.idone = threading.Event()

    def input(self):
        while not self.istopped.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            super().put(event)
        self.idone.set()

    def poll(self):
        "poll for event."
        return self.iqueue.get()

    #def put(self, event):
    #    "put event on iqueue."
    #    self.iqueue.put(event)

    def start(self, daemon=True):
        "start event handler loop."
        super().start()
        self.idone.clear()
        self.istopped.clear()
        Thread.launch(self.input, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        super().stop()
        self.istopped.set()
        self.idone.wait()


class Client(Input):

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
        raise NotImplementedError

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)


class Output(Client):

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

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        super().start(daemon=daemon)
        self.ostopped.clear()
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        self.wait()
        super().stop()
        self.ostopped.set()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            super().wait()
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class Console(Client):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def input(self):
        "polling loop."
        while not self.istopped.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            super().put(event)
            event.wait()
        self.idone.set()

    def poll(self):
        "return event."
        evt = Message()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        return evt

    def raw(self, text):
        "raw output."
        raise NotImplementedError


def __dir__():
    return (
        'Client',
        'Console',
        'Input',
        'Output'
    )
