# This file is placed in the Public Domain.


"encoder/decoder"


import json
import threading
import types


from .objects import Object


class Encoder(json.JSONEncoder):

    lock = threading.RLock()

    def default(self, o):
        "generate serializable versions."
        with Encoder.lock:
            if isinstance(o, type):
                return Object.skip(o)
            if isinstance(o, dict):
                return o.items()
            if isinstance(o, list):
                return iter(o)
            if isinstance(o, types.MappingProxyType):
                return dict(o)
            try:
                return json.JSONEncoder.default(self, o)
            except TypeError:
                try:
                    return vars(o)
                except TypeError:
                    return repr(o)


class Json:

    lock = threading.RLock()

    @classmethod
    def dump(cls, *args, **kw):
        "dump object to disk."
        with cls.lock:
            kw["cls"] = Encoder
            return json.dump(*args, **kw)

    @classmethod
    def dumps(cls, *args, **kw):
        "dump object to string."
        kw["cls"] = Encoder
        return json.dumps(*args, **kw)

    @classmethod
    def load(cls, s, *args, **kw):
        "load object from disk."
        with cls.lock:
            return json.load(s, *args, **kw)

    @classmethod
    def loads(s, *args, **kw):
        "load object from string."
        return json.loads(s, *args, **kw)


def __dir__():
    return (
        'Json',
    )
