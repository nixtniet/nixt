# This file is placed in the Public Domain.


"read/write"


import json
import pathlib
import threading


from .json   import dump, load
from .object import update


lock = threading.RLock()


class DecodeError(Exception):

    pass


def cdir(pth) -> None:
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def read(obj, pth) -> str:
    with lock:
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise DecodeError(pth) from ex
    return pth


def write(obj, pth) -> str:
    with lock:
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return pth


def __dir__():
    return (
        'DecodeError',
        'cdir',
        'read',
        'write'
    )
