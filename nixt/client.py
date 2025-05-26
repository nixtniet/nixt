# This file is placed in the Public Domain.


"client"


import threading


from typing import Dict, ValuesView


from .event   import Event
from .handler import Handler


lock = threading.RLock()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        Fleet.add(self)

    def announce(self, txt: str) -> None:
        pass

    def raw(self, txt: str) -> None:
        raise NotImplementedError("raw")

    def say(self, channel: str, txt: str) -> None:
        self.raw(txt)


class Fleet:

    clients: Dict[str, Client] = {}

    @staticmethod
    def add(clt: Client) -> None:
        Fleet.clients[repr(clt)] = clt

    @staticmethod
    def all() -> ValuesView:
        return Fleet.clients.values()

    @staticmethod
    def announce(txt: str) -> None:
        for clt in Fleet.clients.values():
            clt.announce(txt)

    @staticmethod
    def display(evt: Event) -> None:
        with lock:
            clt = Fleet.get(evt.orig)
            if clt:
                for tme in sorted(evt.result):
                    clt.say(evt.channel, evt.result[tme])
            evt.ready()

    @staticmethod
    def first() -> Client | None:
        clt =  list(Fleet.clients.values())
        res = None
        if clt:
            res = clt[0]
        return res

    @staticmethod
    def get(orig: str) -> Client | None:
        return Fleet.clients.get(orig, None)

    @staticmethod
    def say(orig: str, channel: str, txt: str) -> None:
        clt = Fleet.get(orig)
        if clt:
            clt.say(channel, txt)

    @staticmethod
    def wait() -> None:
        for clt in Fleet.clients.values():
            if "wait" in dir(clt):
                clt.wait()


def __dir__():
    return (
        'Client',
        'Fleet'
    )
