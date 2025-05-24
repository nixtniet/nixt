# This file is placed in the Public Domain.


"decoder/encoder"


from typing import Any, TextIO


import json as jsn


from .object import Object, construct


class Encoder(jsn.JSONEncoder):

    def default(self, o: Any) -> str:
        if isinstance(o, dict):
            return o.items()
        if issubclass(type(o), Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        try:
            return jsn.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return vars(o)
            except TypeError:
                return repr(o)


def dump(obj: Object, fp: TextIO, *args, **kw):
    kw["cls"] = Encoder
    jsn.dump(obj, fp, *args, **kw)


def dumps(obj: Object, *args, **kw):
    kw["cls"] = Encoder
    return jsn.dumps(obj, *args, **kw)


def hook(objdict: dict) -> Object:
    obj = Object()
    construct(obj, objdict)
    return obj


def load(fp: TextIO, *args, **kw) -> Object:
    kw["object_hook"] = hook
    return jsn.load(fp, *args, **kw)


def loads(s: str, *args, **kw) -> Object:
    kw["object_hook"] = hook
    return jsn.loads(s, *args, **kw)


def __dir__():
    return (
        'dump',
        'dumps',
        'hook',
        'load',
        'loads'
    )
