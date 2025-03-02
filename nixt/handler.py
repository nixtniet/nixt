# This file is placed in the Public Domain.


"event handler"


import queue
import threading
import time
import _thread


from .errors import later
from .object import Default
from .thread import launch, name


lock    = threading.RLock()
outlock = threading.RLock()


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


class Handler:

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
            try:
                evt._thr = launch(func, evt, name=(
                                                   evt.txt
                                                   and evt.txt.split()[0]
                                                  ) or name(func)
                                 )
            except Exception as ex:
                later(ex)
                evt.ready()

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                evt = self.queue.get()
                if evt is None:
                    break
                evt.orig = repr(self)
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                evt.ready()
                self.ready,set()
                _thread.interrupt_main()
        self.ready.set()

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


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        Fleet.add(self)

    def announce(self, txt) -> None:
        pass

    def loop(self) -> None:
        evt = None
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                if evt:
                    evt.ready()
                _thread.interrupt_main()
        self.ready.set()

    def poll(self) -> Event:
        return self.queue.get()

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None:
        self.raw(txt)


class Fleet:

    bots = {}

    @staticmethod
    def add(bot) -> None:
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt) -> None:
        for bot in Fleet.bots.values():
            bot.announce(txt)

    @staticmethod
    def display(evt) -> None:
        with outlock:
            for tme in sorted(evt.result):
                Fleet.say(evt.orig, evt.channel, evt.result[tme])
            evt.ready()

    @staticmethod
    def first() -> None:
        bots =  list(Fleet.bots.values())
        res = None
        if bots:
            res = bots[0]
        return res

    @staticmethod
    def get(orig) -> None:
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt) -> None:
        bot = Fleet.get(orig)
        if bot:
            bot.say(channel, txt)

    @staticmethod
    def wait() -> None:
        for bot in Fleet.bots.values():
            if "wait" in dir(bot):
                bot.wait()


def __dir__():
    return (
        'Client',
        'Event',
        'Fleet',
        'Handler'
    )
