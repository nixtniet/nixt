# This file is placed in the Public Domain.


"client pool"


import os
import threading


from .client import Client
from .cmnd   import command
from .fleet  import Fleet
from .output import Output


class Pool:

    clients = []
    lock = threading.RLock()
    nrcpu = os.cpu_count()
    nrlast = 0

    @staticmethod
    def add(clt):
        Pool.clients.append(clt)

    def init(cls):
        for x in range(Pool.nrcpu-1):
            clt = cls()
            clt.start()
            Pool.add(clt)

    @staticmethod
    def put(evt):
       with Pool.lock:
           if Pool.nrlast >= Pool.nrcpu-1:
               Pool.nrlast = 0
           Pool.clients[Pool.nrlast].put(evt)
           Pool.nrlast += 1


def __dir__():
    return (
        'Pool',
    )
