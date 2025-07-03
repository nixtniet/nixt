# This file is placed in the Public Domain.


"clients"


import queue
import threading
import time
import _thread


from .handler import Handler
from .threads import later, launch


class CLI(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock  = threading.RLock()
        Fleet.add(self)

    def announce(self, txt):
        pass

    def display(self, *args):
        with self.olock:
            evt = args[0]
            for tme in sorted(evt.result):
                self.dosay(evt.channel, evt.result[tme])

    def dosay(self, channel, txt):
        self.say(channel, txt)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        self.raw(txt)


class Client(CLI):

    def __init__(self):
        CLI.__init__(self)
        self.oqueue = queue.Queue()
        self.oready = threading.Event()
        self.ostop  = threading.Event()

    def oput(self, evt):
        self.oqueue.put(evt)

    def output(self):
        while not self.ostop.is_set():
            evt = self.oqueue.get()
            if evt is None:
                self.oqueue.task_done()
                break
            self.display(evt)
            self.oqueue.task_done()
        self.oready.set()

    def start(self):
        super().start()
        self.oready.clear()
        self.ostop.clear()
        launch(self.output)

    def stop(self):
        super().stop()
        self.ostop.set()
        self.oqueue.put(None)
        self.oready.wait()

    def wait(self):
        self.oqueue.join()
        super().wait()


class Fleet:

    clients = {}

    @staticmethod
    def add(clt):
        Fleet.clients[repr(clt)] = clt

    @staticmethod
    def all():
        return Fleet.clients.values()

    @staticmethod
    def announce(txt):
        for clt in Fleet.all():
            clt.announce(txt)

    @staticmethod
    def dispatch(evt):
        clt = Fleet.get(evt.orig)
        clt.put(evt)

    @staticmethod
    def display(evt):
        clt = Fleet.get(evt.orig)
        clt.oput(evt)

    @staticmethod
    def first():
        clt =  list(Fleet.all())
        res = None
        if clt:
            res = clt[0]
        return res

    @staticmethod
    def get(orig):
        return Fleet.clients.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        clt = Fleet.get(orig)
        if clt:
            clt.say(channel, txt)

    @staticmethod
    def shutdown():
        for clt in Fleet.all():
            clt.stop()

    @staticmethod
    def wait():
        time.sleep(0.1)
        for clt in Fleet.all():
            clt.wait()


def __dir__():
    return (
        'CLI',
        'Client',
        'Fleet'
    )
