# This file is placed in the Public Domain.


import json as jsn


from typing import Any, TextIO


from .object import Object, construct


class Encoder(jsn.JSONEncoder):

    def default(self, o: Any) -> str: ...


def dump(obj: Object, fp: TextIO, *args, **kw): ...
def dumps(obj: Object, *args, **kw): ...
def hook(objdict: dict): ...
def load(fp: TextIO, *args, **kw): ...
def loads(s: str, *args, **kw): ...
