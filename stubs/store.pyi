# This file is placed in the Public Domain.


"read/write"


import os
import pathlib
import threading


lock = threading.RLock()
p    = os.path.join


class Workdir:

    name: str
    wdr: str


def long(name: str) -> str: ...
def moddir() -> str: ...
def pidname(name) -> str: ...
def skel() -> None: ...
def setwd(pth) -> None: ...
def store(pth: str=""): ...
def strip(pth: str, nmr: int=2): ...
def types() -> list[str]: ...
def wdr(pth: str) -> None: ...


def __dir__():
    return (
        'Workdir',
        'long',
        'moddir',
        'pidname',
        'setwd',
        'skel',
        'store',
        'strip',
        'wdr'
    )
