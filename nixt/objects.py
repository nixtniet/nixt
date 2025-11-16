# This file is placed in the Public Domain.


import json
import types


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def construct(obj, *args, **kwargs):
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        else:
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def items(obj):
    if isinstance(obj, dict):
        return obj.items()
    if isinstance(obj, types.MappingProxyType):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    if isinstance(obj, dict):
        return obj.keys()
    return obj.__dict__.keys()


def update(obj, data={}, empty=True):
    if isinstance(obj, type):
        for k, v in items(data):
            if isinstance(getattr(obj, k, None), types.MethodType):
                continue
            setattr(obj, k, v)
    elif isinstance(obj, dict):
        for k, v in items(data):
            setattr(obj, k, v)
    else:
        for key, value in items(data):
            if not empty and not value:
                continue
            setattr(obj, key, value)


def values(obj):
    if isinstance(obj, dict):
        return obj.values()
    return obj.__dict__.values()



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


def dump(*args, **kw):
    kw["cls"] = Encoder
    return json.dump(*args, **kw)


def dumps(*args, **kw):
    kw["cls"] = Encoder
    return json.dumps(*args, **kw)


def load(s, *args, **kw):
    return json.load(s, *args, **kw)


def loads(s, *args, **kw):
    return json.loads(s, *args, **kw)


def __dir__():
    return (
        'Object',
        'construct',
        'dump',
        'dumps',
        'fqn',
        'items',
        'keys',
        'load',
        'loads',
        'update',
        'values'
    )
