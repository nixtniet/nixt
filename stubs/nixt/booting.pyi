# This file is placed in the Public Domain.


"in the beginning"


import threading
import time
import _thread


from threading import Event
from typing import Callabla


from .clients import Broker, Client
from .command import Commands
from .configs import Main
from .package import Mods
from .persist import Workdir
from .require import Cmd
from .tasking import Task
from .utility import MD5, Log, Logging, Utils


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
    def init(cls, names: str, wait: bool = False): -> None
        ...

    @classmethod
    def shutdown(cls, wait: bool = True) -> None: 
        ...

    @classmethod
    def wrapped(cls, func: Callable, *args) -> None:
        ...

    @classmethod
    def wrap(cls, func" Callable, *args, dofinal: Callable = None) -> None:
        ...


def __dir__():
    return (
        'Boot',
    )
