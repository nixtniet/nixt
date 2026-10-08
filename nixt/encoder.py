# This file is placed in the Public Domain.


"encoder/decoder"


import json
import types


from .default import RLock
from .methods import Method
from .typings import Any, MappingProxyType, Union


Json = Union[dict,list,bool,float,int,str]


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
            if isinstance(o, MappingProxyType):
                return dict(o)
            try:
                return json.JSONEncoder.default(self, o)
            except TypeError:
                try:
                    return self.skip(vars(o))
                except TypeError:
                    return repr(o)

    def skip(self, obj: Any) -> dict:
        "yield values without underscored keys."
        result = {}
        for key, value in Method.items(obj):
            if key.startswith("_"):
                continue
            if isinstance(value, types.MethodType):
                continue
            result[key] = value
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
    def load(cls, s, *args, **kw) -> Json:
        "load object from disk."
        return json.load(s, *args, **kw)

    @classmethod
    def loads(cls, s, *args, **kw) -> Json:
        "load object from string."
        return json.loads(s, *args, **kw)


class JSONL(JSON):

    "line oriented"

    @classmethod
    def read(cls, fp, *args, **kw):
        "read from file."
        return cls.loads(fp, *args, **kw)

    @classmethod
    def write(cls, *args, **kw) -> None:
        "dump object to disk."
        kw["indent"] = None
        kw["skipkeys"] = True
        kw["sort_keys"] = True
        cls.dump(*args, **kw)
        args[1].write("\n")
        args[1].flush()


def __dir__():
    return (
        'JSON',
        'JSONL'
    )
