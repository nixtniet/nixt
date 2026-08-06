# This file is placed in the Public Domain.


"a clean namespace"


import json
import types
import threading


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __delitem__(self, key):
        del self.__dict__[key]

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __str__(self):
        return str(self.__dict__)


class Default(Object):

    def __getattr__(self, key):
        if key in dir(self):
            return self.__getattribute__(self, key)
        return ""


class Encoder(json.JSONEncoder):

    lock = threading.RLock()

    def default(self, o):
        "generate serializable versions."
        with Encoder.lock:
            if isinstance(o, type):
                return Method.skip(o)
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
        "dump object to disk."
        kw["cls"] = Encoder
        return json.dump(*args, **kw)

    @staticmethod
    def dumps(*args, **kw):
        "dump object to string."
        kw["cls"] = Encoder
        return json.dumps(*args, **kw)

    @staticmethod
    def load(s, *args, **kw):
        "load object from disk."
        return json.load(s, *args, **kw)

    @staticmethod
    def loads(s, *args, **kw):
        "load object from string."
        return json.loads(s, *args, **kw)


from .methods import Method 


def __dir__():
    return (
        'Default',
        'Json',
        'Method',
        'Object'
    )
