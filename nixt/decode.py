# This file is placed in the Public Domain.


"decoder/encoder"


import json


from .object import Object, construct


def hook(objdict):
    obj = Object()
    construct(obj, objdict)
    return obj


def load(fp, *args, **kw):
    kw["object_hook"] = hook
    return json.load(fp, *args, **kw)


def loads(s, *args, **kw):
    kw["object_hook"] = hook
    return json.loads(s, *args, **kw)


def __dir__():
    return (
        "load",
        "loads"
    )
