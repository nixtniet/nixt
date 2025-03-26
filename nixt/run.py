# This file is placed in the Public Domain.


"runtime"


import queue
import threading
import time
import traceback
import typing
import _thread


lock = threading.RLock()


class Reactor:

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
            if evt.txt:
                cmd = evt.txt.split(maxsplit=1)[0]
            else:
                cmd = name(func)
            evt._thr = launch(func, evt, name=cmd)

    def loop(self) -> None:
        while not self.stopped.is_set():
            evt = self.poll()
            if evt is None:
                break
            evt.orig = repr(self)
            try:
                self.callback(evt)
            except Exception as ex:
                later(ex)
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


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self.name = thrname
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def run(self) -> None:
        try:
            func, args = self.queue.get()
            self.result = func(*args)
        except Exception as ex:
            later(ex)
            _thread.interrupt_main()

    def join(self, timeout=None) -> typing.Any:
        super().join(timeout)
        return self.result


class Errors:

    name = __file__.rsplit("/", maxsplit=2)[-2]
    errors = []

    @staticmethod
    def format(exc) -> str:
        exctype, excvalue, trb = type(exc), exc, exc.__traceback__
        trace = traceback.extract_tb(trb)
        result = ""
        for i in trace:
            fname = i[0]
            if fname.endswith(".py"):
                fname = fname[:-3]
            linenr = i[1]
            plugfile = fname.split("/")
            mod = []
            for i in plugfile[::-1]:
                mod.append(i)
                if Errors.name in i or "bin" in i:
                    break
            ownname = '.'.join(mod[::-1])
            if ownname.endswith("__"):
                continue
            if ownname.startswith("<"):
                continue
            result += f"{ownname}:{linenr} "
        del trace
        res = f"{exctype} {result[:-1]} {excvalue}"
        if "__notes__" in dir(exc):
            for note in exc.__notes__:
                res += f" {note}"
        return res

    @staticmethod
    def full(exc) -> str:
        return traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__
        )

def later(exc) -> None:
    Errors.errors.append(exc)


def launch(func, *args, **kwargs) -> Thread:
    nme = kwargs.get("name")
    if not nme:
        nme= name(func)
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj) -> str:
    typ = type(obj)
    if '__builtins__' in dir(typ):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


def __dir__():
    return (
        'Errors',
        'Reactor',
        'Thread',
        'later',
        'launch',
        'name'
    )
