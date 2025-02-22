# This file is placed in the Public Domain.


"pool of threads."


import threading
import time


from .threads import launch


lock    = threading.RLock()
started = threading.Event()


class Pool():

    running = {}

    @staticmethod
    def exec(func, *args, **kwargs) -> None:
        with lock:
            thr = launch(func, *args, **kwargs)
            Pool.running[repr(thr)] = (thr, args)
            return thr

    @staticmethod
    def remove(thr):
        with lock:
            try:
                del Pool.running[repr(thr)]
            except KeyError:
                pass

    @staticmethod
    def wait():
        gotcha = []
        with lock:
            for thr, args in Pool.running.values():
                thr.join()
                args[0].wait()
                gotcha.append(thr)
            for thr in gotcha:
                Pool.remove(thr)


def __dir__():
    return (
        'Pool',
    )
