# This file is placed in the Public Domain.


"clientele"


import logging
import queue
import select
import sys
import threading
import _thread


from .brokers import Broker
from .command import Commands
from .handler import Client
from .message import Message
from .threads import Thread


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
            self.working.append(event)
            event.orig = repr(self)
            self.callback(event)
        self.done.set()


class Console(Poller):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def loop(self):
        "input loop."
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

    def poll(self):
        "return event."
        sys.stdout.write("> ")
        sys.stdout.flush()
        while True:
            (input, output, error) = select.select(
                                             [sys.stdin,],
                                             [sys.stdout],
                                             [sys.stderr,]
                                            )
            if error:
                break
            for inp in input:
                evt = Message()
                evt.orig = repr(self)
                evt.text = inp.readline().strip()
                evt.kind = "command"
                return evt

    def start(self, daemon=True):
        super().start(daemon=daemon)


class Output(Poller):

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()
        self.ostopped = threading.Event()

    def output(self):
        "output loop."
        while not self.ostopped.is_set():
            event = self.oqueue.get()
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


def __dir__():
    return (
        'Client',
        'Console',
        'Output',
        'Poller'
    )
