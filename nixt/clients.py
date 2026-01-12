# This file is placed in the Public Domain.


"client event handler"


import logging
import queue
import threading
import _thread


from .brokers import addobj
from .handler import Handler
from .threads import launch


class Client(Handler):

    def __init__(self):
        super().__init__()
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

    def input(self):
        "input loop."
        while True:
            event = self.poll()
            if not event or self.stopped.is_set():
                break
            self.put(event)

    def poll(self):
        "return event."
        return self.iqueue.get()

    def raw(self, text):
        "raw output."
        raise NotImplementedError("raw")

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)

    def start(self):
        "start client loop."
        super().start()
        launch(self.input)

    def stop(self):
        "stop client loop."
        self.stopped.set()
        super().stop()


class Output(Client):

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
        'Output'
    )
