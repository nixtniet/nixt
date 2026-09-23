# This file is placed in the Public Domain.


"collection of runners/clients"


import os
import threading


from typing import Any, ClassVar, List


from .runners import Runner


class Pool:

    "multiple runners."

    runners: ClassVar[List[Runner]] = []
    clazz = Runner
    lock = threading.RLock()
    max = os.cpu_count()
    nrcpu = 1
    nrlast = 0

    @classmethod
    def add(cls, runner: Runner) -> None:
        "add a runner."
        cls.runners.append(runner)

    @classmethod
    def busy(cls) -> bool:
        "see if pool is busy."
        for runner in cls.runners:
            if runner.queue.qsize():
                return True
        return False

    @classmethod
    def init(cls, nrrunners: int, clz: Any = None) -> None:
        "initialze a number of runners."
        if clz:
            cls.clazz = clz
        for _x in range(nrrunners):
            runner = cls.clazz()
            runner.start()
            cls.add(runner)

    @classmethod
    def put(cls, *args: Any) -> None:
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
