# This file is placed in the Public Domain.


"decoder/encoder"


import json
import pathlib
import threading
import typing


from .object import Object, construct, update


lock = threading.RLock()


class DecodeError(Exception):

    pass


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


def load(*args, **kw):
    kw["cls"] = Decoder
    kw["object_hook"] = hook
    return json.load(*args, **kw)


def loads(*args, **kw) -> Object:
    kw["cls"] = Decoder
    kw["object_hook"] = hook
    return json.loads(*args, **kw)


def read(obj, pth):
    with lock:
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise DecodeError(pth) from ex
    return pth


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


def dump(*args, **kw):
    kw["cls"] = Encoder
    json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    kw["cls"] = Encoder
    return json.dumps(*args, **kw)


def write(obj, pth):
    with lock:
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return pth


def cdir(pth) -> None:
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def __dir__():
    return (
        'dump',
        'dumps',
        'load',
        'loads',
        'read',
        'write'
    )
