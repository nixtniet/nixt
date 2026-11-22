# This file is placed in the Public Domain.


"encoder/decoder"


import json
import types


from .imports import RLock


class Encoder(json.JSONEncoder):

    "object to string"

    lock = RLock()

    def default(self, o):
        "generate serializable versions."
        with Encoder.lock:
            try:
                return json.JSONEncoder.default(self, self.skip(o))
            except TypeError:
                pass
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
                    return self.skip(o)
                except TypeError:
                    return repr(o)

    def skip(self, obj):
        "yield values without underscored keys."
        result = {}
        for key in dir(obj):
            if key.startswith("_"):
                continue
            value = getattr(obj, key, None)
            if isinstance(value, types.MethodType):
                continue
            result[key] = value
        return result


class JSON:

    "json wrapper"

    @classmethod
    def dump(cls, *args, **kwargs):
        "dump object to disk."
        kwargs["cls"] = Encoder
        return json.dump(*args, **kwargs)

    @classmethod
    def dumps(cls, *args, **kwargs):
        "dump object to string."
        kwargs["cls"] = Encoder
        return json.dumps(*args, **kwargs)

    @classmethod
    def load(cls, s, *args, **kwargs):
        "load object from disk."
        return json.load(s, *args, **kwargs)

    @classmethod
    def loads(cls, s, *args, **kwargs):
        "load object from string."
        return json.loads(s, *args, **kwargs)


class JSONL(JSON):

    "line oriented"

    @classmethod
    def read(cls, fp, *args, **kwargs):
        "read from file."
        return cls.load(fp, *args, **kwargs)

    @classmethod
    def write(cls, obj, fp, *args, **kwargs):
        "dump object to disk."
        kwargs["indent"] = None
        kwargs["skipkeys"] = True
        kwargs["sort_keys"] = True
        cls.dump(obj, fp, *args, **kwargs)
        fp.write("\n")
        fp.flush()


def __dir__():
    return (
        'JSON',
        'JSONL'
    )
