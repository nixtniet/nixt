# This file is placed in the Public Domain.


"you'd  better run"


import os


from .looping import Loop
from .threads import Thread


class Runner(Loop):

    "run job."

    def run(self, *args, **kwargs):
        "fetch a feed."
        raise NotImplementedError

    def loop(self):
        "loop to handle fetch jobs."
        while not self.stopped.is_set():
            job = self.queue.get()
            if job is None:
                break
            self.run(*job)

    def start(self, daemon=True):
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Thread.launch(self.loop, daemon=daemon, name="Runner.loop")


class Pool:

    "multiple runners."

    clazz = Runner
    runners = []
    max = os.cpu_count()
    nrcpu = 1
    nrlast = 0

    @classmethod
    def add(cls, client):
        "add a runner."
        cls.runners.append(client)

    @classmethod
    def busy(cls):
        for runner in cls.runners:
            if cls.queue.qsize():
                return True
        return False

    @classmethod
    def init(cls, nr, clz=None):
        "initialze a number of runners."
        if clz:
            cls.clazz = clz
        for x in range(nr):
            runner = cls.clazz()
            runner.start()
            cls.add(runner)

    @classmethod
    def put(cls, *args):
        "push job to a runner."
        if not cls.runners:
            return
        if cls.nrlast > cls.nrcpu-1:
            cls.nrlast = 0
        clt = cls.runners[cls.nrlast]
        clt.put(*args)
        cls.nrlast += 1


def __dir__():
    return (
        'Pool',
        'Runner'
    )
