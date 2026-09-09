# This file is placed in the Public Domain.


"you'd  better run"


import os


from .looping import Loop
from .threads import Thread


class Runner(Loop):

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

    def __init__(self, clazz=None):
        self.clazz = clazz or Runner
        self.runners = []
        self.max = os.cpu_count()
        self.nrcpu = 1
        self.nrlast = 0

    def add(self, client):
        "add a runner."
        self.runners.append(client)

    def busy(self):
        for runner in self.runners:
            if runner.queue.qsize():
                return True
        return False

    def init(self, nr):
        "initialze a number of runners."
        for x in range(nr):
            runner = self.clazz()
            runner.start()
            self.add(runner)

    def put(self, *args):
        "push job to a runner."
        if not self.runners:
            return
        if self.nrlast > self.nrcpu-1:
            self.nrlast = 0
        clt = self.runners[self.nrlast]
        clt.put(*args)
        self.nrlast += 1


def __dir__():
    return (
        'Pool',
        'Runner'
    )
