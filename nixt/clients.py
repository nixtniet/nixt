# This file is placed in the Public Domain.


"clients"


import logging
import queue
import threading
import time
import _thread


from .brokers import Broker
from .engines import Engine
from .threads import Thread


class Output:

    block = threading.Event()

    def __init__(self):
        super().__init__()
        self.olock = threading.RLock()
        self.silent = False
        Broker.add(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for txt in event.result:
                if self.block.is_set():
                    return
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


class Buffer(Output):

    def __init__(self):
        Output.__init__(self)
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
        self.ostopped.clear()
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        self.ostopped.set()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class Buffered(Engine, Buffer):

    def __init__(self):
        Engine.__init__(self)
        Buffer.__init__(self)

    def start(self):
        "start buffered client."
        Engine.start(self)
        Buffer.start(self)

    def stop(self):
        "stop buffered client."
        Engine.stop(self)
        Buffer.stop(self)


class Client(Engine, Output):

    def __init__(self):
        Engine.__init__(self)
        Output.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


class Clients:

    @staticmethod
    def announce(txt):
        "announce text on all clients."
        for obj in Broker.objs("announce"):
            obj.announce(txt)

    @staticmethod
    def shutdown():
        "call stop on clients."
        for client in Broker.objs("wait"):
            client.wait()
        time.sleep(0.01)
        for client in Broker.objs("stop"):
            client.stop()
        time.sleep(0.01)


def __dir__():
    return (
        'Buffer',
        'Buffered',
        'Client',
        'Clients',
        'Output'
    )
