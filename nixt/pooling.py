# This file is placed in the Public Domain.


"you'd  better run"


import os


from typing import ClassVar


from .looping import Runner


class Pool:

    "multiple runners."

    clazz = Runner
    runners: ClassVar[list[Runner]] = []
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
            if runner.queue.qsize():
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
    )
