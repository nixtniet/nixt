# This file is placed in the Public Domain.


"in the beginning"


from .default import Event
from .utility import Log


from typing import Callable


logger = Log(__name__)


class Boot:

    "at startup"

    running: Event
    stopped: Event

    @classmethod
    def banner(cls, force: bool = False) -> None:
        ...

    @classmethod
    def boot(cls) -> None:
        ...

    @classmethod
    def configure(cls, wdr="") -> None:
        ...

    @classmethod
    def forever(cls) -> None:
        ...

    @classmethod
    def init(cls, names: str, wait: bool = False) -> None:
        ...

    @classmethod
    def shutdown(cls, wait: bool = True) -> None: 
        ...

    @classmethod
    def wrapped(cls, func: Callable, *args) -> None:
        ...

    @classmethod
    def wrap(cls, func: Callable, *args, dofinal: Callable | None = None) -> None:
        ...


def __dir__():
    ...
