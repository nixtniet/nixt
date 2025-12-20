# This file is placed in the Public Domain.


"handle your own events"


import logging
import queue
import threading
import _thread


from .brokers import ticket
from .command import command
from .threads import launch


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()

    def callback(self, event):
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = launch(func, event, name=name)

    def loop(self):
        while True:
            event = self.poll()
            if not event:
                break
            event.orig = repr(self)
            self.callback(event)

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put(event)

    def register(self, kind, callback):
        self.cbs[kind] = callback

    def start(self):
        launch(self.loop)

    def stop(self):
        self.queue.put(None)


class Client(Handler):

    def __init__(self):
        super().__init__()
        self.olock = threading.RLock()
        self.oqueue = queue.Queue()
        self.silent = True
        ticket(self)

    def announce(self, text):
        if not self.silent:
            self.raw(text)

    def display(self, event):
        with self.olock:
            for tme in event.result:
                txt = event.result.get(tme)
                self.dosay(event.channel, txt)

    def dosay(self, channel, text):
        self.say(channel, text)

    def raw(self, text):
        raise NotImplementedError("raw")

    def say(self, channel, text):
        self.raw(text)

    def wait(self):
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class CLI(Client):

    def __init__(self):
        super().__init__()
        self.register("command", command)


class Output(Client):

    def output(self):
        while True:
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self):
        launch(self.output)
        super().start()

    def stop(self):
        self.oqueue.put(None)
        super().stop()


def __dir__():
    return (
        'CLI',
        'Client',
        'Handler',
        'Output'
    )
