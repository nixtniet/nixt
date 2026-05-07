# This file is placed in the Public Domain.


"event handling"


import queue
import threading


from .brokers import Broker
from .command import Commands
from .handler import Handler
from .parsers import Parse
from .threads import Thread


class Input(Handler):

    def __init__(self):
        super().__init__()
        self.iqueue = queue.Queue()
        self.olock = threading.RLock()
        self.silent = True
        self.stopped = threading.Event()
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

    def loop(self):
        "input loop."
        while self.running.is_set():
            event = self.iqueue.get()
            if not event:
                break
            event.orig = repr(self)
            self.callback(event)

    def put(self, event):
        "put event into queue."
        self.iqueue.put(event)

    def raw(self, text):
        "raw output."

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)

    def stop(self):
        "stop client."
        super().stop()
        self.running.clear()
        self.iqueue.put(None)


class Polled(Input):

    def loop(self):
        "polling loop."
        while self.running.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            event.orig = repr(self)
            self.callback(event)

    def poll(self):
        "return event."
        return self.iqueue.get()


class Console(Polled):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def loop(self):
        "input loop."
        while self.running.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            event.orig = repr(self)
            self.callback(event)
            event.wait()


class Client(Polled):

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()

    def output(self):
        "output loop."
        while self.running.is_set():
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self, daemon=True):
        "start output loop."
        super().start()
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        super().stop()
        self.oqueue.put(None)

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
        'Client',
        'Console',
        'Event',
        'Handler'
    )
