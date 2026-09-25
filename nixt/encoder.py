# This file is placed in the Public Domain.


"encoder/decoder"


import json
import types


from threading import RLock
from typing    import Union


jsontypes = Union[dict,list,bool,float,int,str]


class Encoder(json.JSONEncoder):

    "object to string"

    lock: RLock = RLock()

    def default(self, o):
        "generate serializable versions."
        with Encoder.lock:
            if isinstance(o, type):
                return self.skip(o)
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

    def skip(self, obj: object) -> dict:
        "yield values without underscored keys."
        result = {}
        for key in dir(obj):
            if key.startswith("_"):
                continue
            result[key] = getattr(obj, key)
        return result


class JSON:

    "json wrapper"

    @classmethod
    def dump(cls, *args, **kw) -> None:
        "dump object to disk."
        kw["cls"] = Encoder
        return json.dump(*args, **kw)

    @classmethod
    def dumps(cls, *args, **kw) -> str:
        "dump object to string."
        kw["cls"] = Encoder
        return json.dumps(*args, **kw)

    @classmethod
    def load(cls, s, *args, **kw) -> jsontypes:
        "load object from disk."
        return json.load(s, *args, **kw)

    @classmethod
    def loads(cls, s, *args, **kw) -> jsontypes:
        "load object from string."
        return json.loads(s, *args, **kw)


class JSONL(JSON):

    "line oriented"

    @classmethod
    def log(cls, *args, **kw) -> None:
        "dump object to disk."
        kw["indent"] = None
        JSON.dump(cls, *args, **kw)

    @classmethod
    def logtxt(cls, *args, **kw) -> str:
        "dump object to string."
        kw["indent"] = None
        return JSON.dumps(*args, **kw)


def __dir__():
    return (
        'JSON',
        'JSONL'
    )
