# This file is placed in the Public Domain.


from threading import RLock
from typing import Dict


from .client import Client
from .event  import Event


lock = RLock()


class Fleet:

    clients = Dict[str, Client]

    @staticmethod
    def add(clt: Client): ...

    @staticmethod
    def all(): ...

    @staticmethod
    def announce(txt: str): ...

    @staticmethod
    def display(evt: Event): ...

    @staticmethod
    def first() -> Client: ...

    @staticmethod
    def get(orig: str) -> Client: ...

    @staticmethod
    def say(orig: str, channel: str, txt: str) -> None: ...

    @staticmethod
    def wait() -> None: ...
