# This file is placed in the Public Domain.


"runtime"


import logging
import os
import queue
import threading
import time
import _thread


from .methods import name


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


class Thread(threading.Thread):

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.name = kwargs.get("name", name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def run(self):
        func, args = self.queue.get()
        try:
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()

    def join(self, timeout=None):
        try:
            super().join(timeout)
            return self.result
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


"workers"


class Worker:

    def __init__(self):
        self.lock  = threading.RLock()
        self.queue = queue.Queue()
        self.stop  = threading.Event()

    def put(self, func, args):
        self.queue.put((func, args))

    def run(self):
        while not self.stop.is_set():
            func, args = self.queue.get()
            if func is None and args is None:
                self.queue.task_done()
                break
            try:
                func(*args)
            except Exception as ex:
                logging.exception(ex)
                _thread.interrupt_main()
            self.queue.task_done()

    def start(self):
        self.stop.clear()
        launch(self.run)

    def stop(self):
        self.stop.set()
        self.queue.put((None, None))

    def wait(self):
        try:
            self.queue.join()
        except Exception as ex:
            _thread.interrupt_main()


class Pool:

    workers = []
    lock = threading.RLock()
    nrcpu = os.cpu_count()
    nrlast = 0

    @staticmethod
    def add(wrk):
        Pool.workers.append(wrk)

    @staticmethod
    def init(nr=None):
        Pool.nrcpu = nr or os.cpu_count
        for x in range(Pool.nrcpu):
            Pool.new()

    @staticmethod
    def new():
        worker = Worker()
        worker.start()
        Pool.add(worker)
        return worker

    @staticmethod
    def put(func, args):
        with Pool.lock:
            if not Pool.workers:
                Pool.new()
            gotcha = False
            for worker in Pool.workers:
                if worker.queue.qsize() == 0:
                    worker.put(func, args)
                    gotcha = True
            if not gotcha:
                if len(Pool.workers) < Pool.nrcpu:
                    worker = Pool.new()
                    worker.put(func, args)
                else:
                    Pool.nrlast = 0
                    worker= Pool.workers[Pool.nrlast]
                    worker.put(func, args)
                    Pool.nrlast += 1

    @staticmethod
    def shutdown():
        with Pool.lock:
            for worker in Pool.workers:
                worker.stop()


"timer/repeater"


class Timy(threading.Timer):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(sleep, func)
        self.name = kwargs.get("name", name(func))
        self.sleep = sleep
        self.state = {}
        self.state["latest"] = time.time()
        self.state["starttime"] = time.time()
        self.starttime = time.time()


class Timed:

    def __init__(self, sleep, func, *args, thrname="", **kwargs):
        self.args = args
        self.func = func
        self.kwargs = kwargs
        self.sleep = sleep
        self.name = thrname or kwargs.get("name", name(func))
        self.target = time.time() + self.sleep
        self.timer = None

    def run(self):
        self.timer.latest = time.time()
        self.func(*self.args)

    def start(self):
        self.kwargs["name"] = self.name
        timer = Timy(self.sleep, self.run, *self.args, **self.kwargs)
        timer.start()
        self.timer = timer

    def stop(self):
        if self.timer:
            self.timer.cancel()


class Repeater(Timed):

    def run(self):
        launch(self.start)
        super().run()


"utility"


def dispatch(func, *args, **kwargs):
    Pool.put(func, args)


def launch(func, *args, **kwargs):
    thread = Thread(func, *args, **kwargs)
    thread.start()
    return thread


def level(loglevel="debug"):
    if loglevel != "none":
        format_short = "%(asctime)-8s %(message)-80s"
        datefmt = "%H:%M:%S"
        logging.basicConfig(datefmt=datefmt, format=format_short, force=True)
        logging.getLogger().setLevel(LEVELS.get(loglevel))


def rlog(loglevel, txt, ignore=None):
    if ignore is None:
        ignore = []
    for ign in ignore:
        if ign in str(txt):
            return
    logging.log(LEVELS.get(loglevel), txt)


"interface"


def __dir__():
    return (
        'Pool',
        'Repeater',
        'Thread',
        'Timed',
        'launch',
        'level',
        'rlog'
   )
