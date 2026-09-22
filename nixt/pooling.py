# This file is placed in the Public Domain.


"collection of runners/clients"


import os


from typing import ClassVar, List


from .runners import Runner


class Pool:

    "multiple runners."

    clazz = Runner
    runners: ClassVar[List[Runner]] = []
    max = os.cpu_count()
    nrcpu = 1
    nrlast = 0

    @classmethod
    def add(cls, client):
        "add a runner."
        cls.runners.append(client)

    @classmethod
    def busy(cls):
        "see if pool is busy."
        for runner in cls.runners:
            if runner.queue.qsize():
                return True
        return False

    @classmethod
    def init(cls, nr, clz=None):
        "initialze a number of runners."
        if clz:
            cls.clazz = clz
        for _x in range(nr):
            runner = cls.clazz()
            runner.start()
            cls.add(runner)

    @classmethod
    def put(cls, *args):
        "push job to a runner."
        print(cls.nrlast, cls.runners)
        if cls.nrlast-1 >= len(cls.runners)-1:
            cls.nrlast = 0
        clt = cls.runners[cls.nrlast-1]
        clt.put(*args)
        cls.nrlast += 1


def __dir__():
    return (
        'Pool',
    )
