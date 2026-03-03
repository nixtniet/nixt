# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0105,W0613,
# pylint: disable=W0212,W0718,E0402


"callback engine"


import logging
import queue
import threading
import time
import _thread


from .threads import launch


"message"


class Event:

    def __init__(self):
        self._ready = threading.Event()
        self._thr = None
        self.result = {}
        self.args = []
        self.index = 0
        self.kind = "event"
        self.orig = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __str__(self):
        return str(self.__dict__)

    def ready(self):
        "flag message as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result[time.time()] = text

    def wait(self, timeout=0.0):
        "wait for completion."
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout)


"broker"


class Broker:

    objects = {}

    def add(self, obj):
        "add object to the broker, key is repr(obj)."
        self.objects[repr(obj)] = obj

    def announce(self, txt):
        "announce text on all objects with an announce method."
        for obj in self.objs("announce"):
            obj.announce(txt)

    def get(self, origin):
        "object by repr(obj)."
        return self.objects.get(origin)

    def objs(self, attr):
        "objects with a certain attribute."
        for obj in self.objects.values():
            if attr in dir(obj):
                yield obj

    def has(self, obj):
        "whether the broker has object."
        return repr(obj) in self.objects

    def like(self, txt):
        "all keys with a substring in their key."
        for orig in self.objects:
            if txt in orig.split()[0]:
                yield orig

    @staticmethod
    def register(obj):
        Broker.objects[repr(obj)] = obj


"handler"


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.running = threading.Event()

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
        while self.running.is_set():
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
        self.running.set()
        launch(self.loop, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        self.running.clear()
        self.queue.put(None)


"client"


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.iqueue = queue.Queue()
        self.olock = threading.RLock()
        self.silent = False
        self.stopped = threading.Event()
        Broker.register(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for tme in event.result:
                self.dosay(event.channel, event.result.get(tme))
            event.ready()

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


"console"


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

"buffered"


class Output(Client):

    def __init__(self):
        Client.__init__(self)
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

    def start(self, daemon=True):
        "start output loop."
        launch(self.output, daemon=daemon)
        Client.start(self, daemon=daemon)

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


"interface"


def __dir__():
    return (
        'Broker',
        'Client',
        'Console',
        'Event',
        'Handler',
        'Output'
    )
