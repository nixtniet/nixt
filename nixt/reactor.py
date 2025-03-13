# This file is placed in the Public Domain.


"callback engine"


import queue
import threading
import time


import _thread


from .errors import later
from .fleet  import Fleet
from .object import Default
from .thread import launch, name


lock    = threading.RLock()
outlock = threading.RLock()


class Reactor:

    bork = False
    threaded = True

    def __init__(self):
        self.cbs     = {}
        self.queue   = queue.Queue()
        self.ready   = threading.Event()
        self.stopped = threading.Event()

    def callback(self, evt) -> None:
        with lock:
            func = self.cbs.get(evt.type, None)
            if not func:
                evt.ready()
                return
            if not Reactor.threaded:
                func(evt)
                return
            evt._thr = launch(func, evt, name=(
                                               evt.txt
                                               and evt.txt.split()[0]
                                              ) or name(func)

                             )

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                self.callback(evt)
            except Exception as ex:
                later(ex)
                evt.ready()
                if Reactor.bork:
                    _thread.interrupt_main()
        self.ready.set()

    def poll(self):
        return self.queue.get()

    def put(self, evt) -> None:
        self.queue.put(evt)

    def register(self, typ, cbs) -> None:
        self.cbs[typ] = cbs

    def start(self) -> None:
        self.stopped.clear()
        self.ready.clear()
        launch(self.loop)

    def stop(self) -> None:
        self.stopped.set()
        self.queue.put(None)

    def wait(self) -> None:
        self.ready.wait()


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)

    def announce(self, txt) -> None:
        pass

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None:
        self.raw(txt)


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.result = {}
        self.type   = "event"
        self.txt    = ""

    def display(self) -> None:
        Fleet.display(self)

    def done(self) -> None:
        self.reply("ok")

    def ready(self) -> None:
        self._ready.set()

    def reply(self, txt) -> None:
        self.result[time.time()] = txt

    def wait(self) -> None:
        self._ready.wait()
        if self._thr:
            self._thr.join()



def __dir__():
    return (
        'Client',
        'EVent',
        'Handler',
        'Reactor'
    )
