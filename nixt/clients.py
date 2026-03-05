# This file is placed in the Public Domain.


"callback engine"


import logging
import queue
import threading
import _thread


from .handler import Handler
from .threads import Thread


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.iqueue = queue.Queue()
        self.olock = threading.RLock()
        self.silent = False
        self.stopped = threading.Event()
        Broker.add(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for tme in event.result:
                self.dosay(event.channel, event.result.get(tme))

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def loop(self):
        "input loop."
        while True:
            event = self.poll()
            if not event or self.stopped.is_set():
                break
            event.orig = repr(self)
            self.callback(event)

    def poll(self):
        "return event."
        return self.iqueue.get()

    def put(self, event):
        self.iqueue.put(event)

    def raw(self, text):
        "raw output."

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
        Thread.launch(self.output)

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


class Broker:

    objects = {}

    @staticmethod
    def add(obj):
        "add object to the broker, key is repr(obj)."
        Broker.objects[repr(obj)] = obj

    @staticmethod
    def announce(txt):
        "announce text on all objects with an announce method."
        for obj in Broker.objs("announce"):
            obj.announce(txt)

    @staticmethod
    def get(origin):
        "object by repr(obj)."
        return Broker.objects.get(origin)

    @staticmethod
    def objs(attr):
        "objects with a certain attribute."
        for obj in Broker.objects.values():
            if attr in dir(obj):
                yield obj

    @staticmethod
    def has(obj):
        "whether the Broker has object."
        return repr(obj) in Broker.objects

    @staticmethod
    def like(txt):
        "all keys with a substring in their key."
        for orig in Broker.objects:
            if txt in orig.split()[0]:
                yield orig


def __dir__():
    return (
        'Broker',
        'Client',
        'Console',
        'Output'
    )
