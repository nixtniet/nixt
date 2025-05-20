# This file is placed in the Public Domain.


"list of clients"


import threading


lock = threading.RLock()


class Fleet:

    clients = {}

    @staticmethod
    def add(clt: str) -> Client: ...

    @staticmethod
    def all(): ...

    @staticmethod
    def announce(txt: str): ...

    @staticmethod
    def display(evt: Event): ...

    @staticmethod
    def first() -> Client: ...

    @staticmethod
    def get(orig: str) -> Client:
        return Fleet.clients.get(orig, None)

    @staticmethod
    def say(orig: str, channel: str, txt: str) -> None: ...

    @staticmethod
    def wait() -> None: ...


def __dir__():
    return (
        'Fleet',
    )
