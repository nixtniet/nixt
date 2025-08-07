# This file is placed in the Public Domain.


"client pool"


import os
import threading
import time


from .client import Client
from .cmnd   import command
from .fleet  import Fleet
from .output import Output


class Pool:

    clients = []
    lock = threading.RLock()
    nrcpu = 1
    nrlast = 0

    @staticmethod
    def add(clt):
        Pool.clients.append(clt)

    def init(cls, nr=None):
        Pool.nrcpu = nr or os.cpu_count
        for x in range(Pool.nrcpu):
            clt = cls()
            clt.start()
            Pool.add(clt)

    @staticmethod
    def put(evt):
        with Pool.lock:
            if Pool.nrlast >= Pool.nrcpu-1:
                Pool.nrlast = 0
            clt = Pool.clients[Pool.nrlast]
            clt.put(evt)
            Pool.nrlast += 1


def __dir__():
    return (
        'Pool',
    )
