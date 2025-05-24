# This file is placed in the Public Domain.


"event handler"


import _thread


from threading import Event as IEvent
from threading import RLock
from queue     import Queue
from typing    import Callable


from .event  import Event
from .thread import later, launch, name


lock = RLock()


class Handler:

    def __init__(self):
        self.cbs     = {}
        self.queue   = Queue() 
        self.ready   = IEvent()
        self.stopped = IEvent()

    def callback(self, evt: Event) -> None:
        with lock:
            func = self.cbs.get(evt.type, None)
            if not func:
                evt.ready()
                return
            if evt.txt:
                cmd = evt.txt.split(maxsplit=1)[0]
            else:
                cmd = name(func)
            evt._thr = launch(func, evt, name=cmd)

    def loop(self):
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                self.callback(evt)
            except Exception as ex:
                self.stopped.set()
                later(ex)
                _thread.interrupt_main()
        self.ready.set()

    def poll(self):
        return self.queue.get()

    def put(self, evt: Event):
        self.queue.put(evt)

    def register(self, typ: str, cbs: Callable):
        self.cbs[typ] = cbs

    def start(self):
        self.stopped.clear()
        self.ready.clear()
        launch(self.loop)

    def stop(self):
        self.stopped.set()
        self.queue.put(None)

    def wait(self):
        self.ready.wait()


def __dir__():
    return (
        'Handler',
    )
