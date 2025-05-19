# This file is placed in the Public Domain.


"list of clients"


from typing import Any


class Fleet:

    clients = {}

    @staticmethod
    def add(clt) -> None: ...
    @staticmethod
    def all() -> list[Any]: ...
    @staticmethod
    def announce(txt) -> None: ...
    @staticmethod
    def display(evt) -> None: ...
    @staticmethod
    def first() -> None: ...
    @staticmethod
    def get(orig) -> None: ...
    @staticmethod
    def say(orig, channel, txt) -> None: ...
    @staticmethod
    def wait() -> None: ...
