# This file is placed in the Public Domain.


"client"


from .fleet   import Fleet
from .handler import Handler


class Client(Handler):

    def __init__(self): ...
    def announce(self, txt: str) -> None: ...
    def raw(self, txt: str) -> None: ...
    def say(self, channel: str, txt: str) -> None: ...
