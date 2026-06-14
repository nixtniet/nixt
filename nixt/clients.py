# This file is placed in the Public Domain.


"clients"


import logging
import os
import queue
import threading
import time
import _thread


from .brokers import Broker
from .handler import Handler
from .threads import Thread


class Output:

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

    def wait(self):
        "bogus wait."


class Buffer(Output):

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
        self.ostopped.clear()
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        #self.wait()
        self.ostopped.set()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        print(f"wait {str(self)}")
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class Buffered(Handler, Buffer):

    def __init__(self):
        Handler.__init__(self)
        Buffer.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        Handler.start(self)
        Buffer.start(self, daemon=daemon)

    def stop(self):
        "stop output loop."
        Handler.stop(self)
        Buffer.stop(self)


class Client(Handler, Output):

    def __init__(self):
        Handler.__init__(self)
        Output.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


class ClientPool:

    clients = []
    lock = threading.RLock()
    last = 0
    nrevents = 0
    nrcpu = 1

    @classmethod
    def add(cls, client):
        "add a client to the pool."
        cls.clients.append(client)

    @classmethod
    def init(cls, client):
        "initialize pool with nr_cpu clients."
        with cls.lock:
            cls.nrcpu = os.cpu_count()
            for _x in range(cls.nrcpu):
                clt = client()
                clt.start()
                cls.add(clt)

    @classmethod
    def put(cls, *args):
        "put job to the pool."
        with cls.lock:
            if cls.last >= cls.nrcpu-1:
                cls.last = 0
            cls.clients[cls.last].put(*args)
            cls.last += 1
            cls.nrevents += 1

    @classmethod
    def shutdown(cls):
        for client in cls.clients:
            client.wait()
        time.sleep(0.01)
        for client in cls.clients:
            client.stop()
        time.sleep(0.01)


def __dir__():
    return (
        'Buffer',
        'Buffered',
        'Client',
        'ClientPool',
        'Output'
    )
