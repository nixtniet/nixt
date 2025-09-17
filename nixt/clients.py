# This file is placed in the Public Domain.
# pylint: disable=W0613,W0718


"clients"


import queue
import threading
import time
import _thread


from nixt.runtime import Handler, launch


class Client(Handler):

    "Client"

    def __init__(self):
        Handler.__init__(self)
        self.olock = threading.RLock()
        Fleet.add(self)

    def announce(self, txt):
        "announce text."

    def display(self, event):
        "display an event."
        with self.olock:
            for tme in sorted(event.result):
                self.dosay(event.channel, event.result[tme])

    def dosay(self, channel, txt):
        "remote echo text on channel."
        self.say(channel, txt)

    def raw(self, txt):
        "overload this."
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        "echo test in channel."
        self.raw(txt)


class Output(Client):

    "Output"

    def __init__(self):
        Client.__init__(self)
        self.oqueue = queue.Queue()
        self.ostop  = threading.Event()

    def oput(self, event):
        "put event on output queue."
        self.oqueue.put(event)

    def output(self):
        "output loop."
        while not self.ostop.is_set():
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def raw(self, txt):
        "echo text."
        raise NotImplementedError("raw")

    def start(self, daemon=True):
        "start output loop."
        self.ostop.clear()
        launch(self.output, daemon=daemon)
        super().start()

    def stop(self):
        "stop output loop."
        self.ostop.set()
        self.oqueue.put(None)
        super().stop()

    def wait(self):
        "wait for output queue to be empty."
        try:
            self.oqueue.join()
        except Exception:
            _thread.interrupt_main()


class Fleet:

    "list of clients."

    clients = {}

    @staticmethod
    def add(client):
        "add a clients to he fleet."
        Fleet.clients[repr(client)] = client

    @staticmethod
    def all():
        "return all clients."
        return list(Fleet.clients.values())

    @staticmethod
    def announce(txt):
        "announce text on all clients."
        for client in Fleet.all():
            client.announce(txt)

    @staticmethod
    def dispatch(evt):
        "put event on handler queue."
        client = Fleet.get(evt.orig)
        client.put(evt)

    @staticmethod
    def display(evt):
        "display event on originating client."
        client = Fleet.get(evt.orig)
        client.display(evt)

    @staticmethod
    def first():
        "return first client."
        clt = list(Fleet.all())
        res = None
        if clt:
            res = clt[0]
        return res

    @staticmethod
    def get(orig):
        "return client by origin."
        return Fleet.clients.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        "echo text on originating client."
        client = Fleet.get(orig)
        if client:
            client.say(channel, txt)

    @staticmethod
    def shutdown():
        "stop all clients."
        for client in Fleet.all():
            client.stop()

    @staticmethod
    def wait():
        "wait for all clients to finish."
        time.sleep(0.1)
        for client in Fleet.all():
            client.wait()


def __dir__():
    return (
        'Client',
        'Event',
        'Fleet',
        'Handler',
        'Output'
   )
