# This file is placed in the Public Domain.


"event handler"


import queue
import threading
import time
import _thread


from .errors import later
from .thread import launch, name


lock = _thread.allocate_lock()


class Handler:

    def __init__(self):
        self.cbs     = {}
        self.queue   = queue.Queue()
        self.ready   = threading.Event()
        self.stopped = threading.Event()

    def callback(self, evt):
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
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            except Exception as ex:
                later(ex)
                _thread.interrupt_main()
        self.ready.set()

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put(evt)

    def register(self, typ, cbs):
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



class Event:

    def __init__(self):
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.orig   = ""
        self.result = {}
        self.type   = "event"
        self.txt    = ""

    def __contains__(self, key):
        return key in dir(self)

    def __getattr__(self, key):
        if key not in self:
            setattr(self, key, "")
        return self.__dict__.get(key, "")

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def display(self):
        with lock:
            clt = Fleet.get(self.orig)
            if clt:
                for tme in sorted(self.result):
                    clt.say(self.channel, self.result[tme])
            self.ready()

    def done(self):
        self.reply("ok")

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result[time.time()] = txt

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()


def __dir__():
    return (
        'Event',
        'Handler',
    )
