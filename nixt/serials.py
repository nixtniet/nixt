# This file is placed in the Public Domain.


"realisation of serialisation"


import json
import types


class Encoder(json.JSONEncoder):

    def default(self, o):
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

    @staticmethod
    def dump(*args, **kw):
        kw["cls"] = Encoder
        return json.dump(*args, **kw)

    @staticmethod
    def dumps(*args, **kw):
        kw["cls"] = Encoder
        return json.dumps(*args, **kw)

    @staticmethod
    def load(s, *args, **kw):
        return json.load(s, *args, **kw)

    @staticmethod
    def loads(s, *args, **kw):
        return json.loads(s, *args, **kw)


def __dir__():
   return (
       'Json',
   )
