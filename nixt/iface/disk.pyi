# This file is placed in the Public Domain.


"persistence"


import datetime
import json.decoder
import os
import pathlib
import threading
import types


from .json   import dump, load
from .object import Object, fqn, update
from .store  import store


lock = threading.RLock()
p    = os.path.join


class Error(Exception): ...


class Cache:

    objs = {}

    @staticmethod
    def add(path: str, obj: Object): ...

    @staticmethod
    def get(path: str) -> Object: ...

    @staticmethod
    def typed(matcher: str) -> list[Object]:


def cdir(path: str) -> None: ...
def getpath(obj: Object) -> str: ...
def ident(obj: Object) -> str: ...
def read(obj: Object, path: str) -> None: ...
def write(obj: Object, path: str = ""): ...


def __dir__():
    return (
        'Cache',
        'Error',
        'cdir',
        'getpath',
        'ident',
        'read',
        'write'
    )
