# This file is placed in the Public Domain.


"runners/clients"


import os


from .generic import RLock
from .handler import Loop
from .methods import Methods


class Workers:

    "multiple workers"

    workers = []
    lock = RLock()
    max = os.cpu_count()
    nrcpu = 1
    nrlast = 0

    @classmethod
    def add(cls, worker):
        "add a runner."
        cls.workers.append(worker)

    @classmethod
    def busy(cls):
        "see if pool is busy."
        return any(worker.queue.qsize() for worker in cls.workers)

    @classmethod
    def init(cls, nrs, clz):
        "initialze a number of runners."
        cls.nrcpu = nrs
        for nr in range(nrs):
            worker = clz()
            worker.start(name=f"{Methods.clsname(worker)}{nr}")
            cls.add(worker)

    @classmethod
    def put(cls, *args):
        "push job to a runner."
        with cls.lock:
            if cls.nrlast-1 >= len(cls.workers)-1:
                cls.nrlast = 0
            clt = cls.workers[cls.nrlast-1]
            clt.put(*args)
            cls.nrlast += 1


class Worker(Loop):

    "run jobs"

    def run(self, *args, **kwargs):
        "running."

    def loop(self):
        "loop to handle fetch jobs."
        while not self.stopped.is_set():
            job = self.queue.get()
            if job is None:
                break
            self.run(*job)
        self.done.set()

    def wait(self):
        "skip wait."


def __dir__():
    return (
        'Workers',
        'Worker'
    )
