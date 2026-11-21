# This file is placed in the Public Domain.


"message handler"


from .generic import Event, Queue
from .tasking import Task


class Handler:

    "keep looping"

    def __init__(self):
        self.cbs = {}
        self.queue = Queue()
        self.stopped = Event()
        self.done = Event()

    def after(self, msg):
        "called after callback."

    def handle(self, msg):
        "run callback function with msg."
        func = self.cbs.get(msg.kind, None)
        if not func:
            msg.ready()
            return
        name = msg.text and msg.text.split()[0]
        msg.thread(Task.start(func, msg, name=name))

    def loop(self):
        "callback loop."
        while not self.stopped.is_set():
            self.poll()
            msg = self.queue.get()
            if msg is None:
                self.queue.task_done()
                break
            msg.orig = repr(self)
            self.handle(msg)
            self.after(msg)
            self.queue.task_done()
        self.done.set()

    def poll(self):
        "create msg and put it on the queue."

    def put(self, msg):
        "put msg on queue."
        self.queue.put(msg)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self, **kwargs):
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Task.start(self.loop, **kwargs)

    def stop(self):
        "stop xallback loop."
        self.stopped.set()
        self.queue.put(None)
        self.done.wait()

    def wait(self):
        "wait for all msgs to finish."
        try:
            self.queue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Worker(Handler):

    "run jobs"

    def work(self, *args, **kwargs):
        "running."

    def loop(self):
        "loop to handle fetch jobs."
        while not self.stopped.is_set():
            job = self.queue.get()
            if job is None:
                break
            self.work(*job)
        self.done.set()

    def wait(self):
        "skip wait."




def __dir__():
    return (
        'Handler',
        'Work'
    )
