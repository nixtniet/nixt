# This file is placed in the Public Domain.


"a callback engine as handler"


import logging
import queue
import threading
import _thread


from .brokers import addobj
from .threads import launch


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()

    def callback(self, event):
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = launch(func, event, name=name)

    def loop(self):
        "event loop."
        while True:
            event = self.queue.get()
            if not event:
                break
            event.orig = repr(self)
            self.callback(event)

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self, daemon=True):
        "start event handler loop."
        launch(self.loop, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        self.queue.put(None)


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.iqueue = queue.Queue()
        self.olock = threading.RLock()
        self.silent = True
        self.stopped = threading.Event()
        addobj(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for tme in event.result:
                txt = event.result.get(tme)
                self.dosay(event.channel, txt)

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def raw(self, text):
        "raw output."
        raise NotImplementedError("raw")

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)


class Console(Client):

    def loop(self):
        "input loop."
        while True:
            event = self.poll()
            if not event or self.stopped.is_set():
                break
            event.orig = repr(self)
            self.callback(event)
            event.wait()

    def poll(self):
        "return event."
        return self.iqueue.get()


class Output(Console):

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()

    def output(self):
        "output loop."
        while True:
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self):
        "start output loop."
        super().start()
        launch(self.output)

    def stop(self):
        "stop output loop."
        super().stop()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Client',
        'Console',
        'Handler',
        'Output'
    )
