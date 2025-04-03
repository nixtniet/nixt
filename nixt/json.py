# This file is placed in the Public Domain.


"a clean namespace"


import json


from .object import Object, construct


class Decoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        val = json.JSONDecoder.decode(self, s)
        if isinstance(val, dict):
            return hook(val)
        return val


def hook(objdict) -> Object:
    obj = Object()
    construct(obj, objdict)
    return obj


def loads(string, *args, **kw) -> Object:
    kw["cls"] = Decoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


class Encoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o) -> str:
        if isinstance(o, dict):
            return o.items()
        if issubclass(type(o), Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return vars(o)
            except TypeError:
                return repr(o)


def dumps(*args, **kw) -> str:
    kw["cls"] = Encoder
    return json.dumps(*args, **kw)


def __dir__():
    return (
        'dumps',
        'loads'
    )
