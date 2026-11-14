# This file is placed in the Public Domain.


"runners/clients"


import os


from .methods import Methods
from .utility import RLock


class Pool:

    "multiple runners"

    runners = []
    lock = RLock()
    max = os.cpu_count()
    nrcpu = 1
    nrlast = 0

    @classmethod
    def add(cls, runner):
        "add a runner."
        cls.runners.append(runner)

    @classmethod
    def busy(cls):
        "see if pool is busy."
        return any(runner.queue.qsize() for runner in cls.runners)

    @classmethod
    def init(cls, nrs, clz):
        "initialze a number of runners."
        cls.nrcpu = nrs
        for nr in range(nrs):
            runner = clz()
            runner.start(name=Methods.clsname(runner))
            cls.add(runner)

    @classmethod
    def put(cls, *args):
        "push job to a runner."
        with cls.lock:
            if cls.nrlast-1 >= len(cls.runners)-1:
                cls.nrlast = 0
            clt = cls.runners[cls.nrlast-1]
            clt.put(*args)
            cls.nrlast += 1


def __dir__():
    return (
        'Pool',
    )
