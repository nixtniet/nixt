# This file is placed in the Public Domain.


"locate"


import os
import time
import types


from typing import Iterator

from .disk   import Cache, read
from .object import Object, fqn, items, update
from .store  import long, skel, store


def fns(clz: str) -> Iterator[str]: ...
def fntime(daystr: str) -> float: ...
def find(clz: str, selector: dict={}, deleted: bool=False, matching: bool=False) -> list[[str, Object]]: ...
def isdeleted(obj: Object) -> bool: ...
def last(obj: Object, selector: dict={}): ...
def search(obj, selector, matching:dict{}):


def __dir__():
    return (
        'find',
        'fns',
        'fntime',
        'ident',
        'last',
        'search'
    )
