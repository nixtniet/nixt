# This file is placed in the Public Domain.


"a clean namespace"


import json


class Object:

    "object"

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def construct(obj, *args, **kwargs):
    "construct object from arguments."
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        elif isinstance(val, Object):
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def items(obj):
    "return items of object,"
    if isinstance(obj, dict):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    "return keys of object."
    if isinstance(obj, dict):
        return obj.keys()
    return obj.__dict__.keys()


def update(obj, data, empty=True):
    "update object."
    for key, value in items(data):
        if not empty and not value:
            continue
        setattr(obj, key, value)

def values(obj):
    "return values from object."
    if isinstance(obj, dict):
        return obj.values()
    return obj.__dict__.values()


class Encoder(json.JSONEncoder):

    "encoder"

    def default(self, o):
        "return setializable version."
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


def dump(obj, fp, *args, **kw):
    "dump object to file."
    kw["cls"] = Encoder
    json.dump(obj, fp, *args, **kw)


def dumps(obj, *args, **kw):
    "dump object to string."
    kw["cls"] = Encoder
    return json.dumps(obj, *args, **kw)


def hook(objdict):
    "wrao dict in an object."
    obj = Object()
    construct(obj, objdict)
    return obj


def load(fp, *args, **kw):
    "load object from file."
    kw["object_hook"] = hook
    return json.load(fp, *args, **kw)


def loads(s, *args, **kw):
    "load object from string."
    kw["object_hook"] = hook
    return json.loads(s, *args, **kw)


def __dir__():
    return (
        'Object',
        'construct',
        'dump',
        'dumps',
        'items',
        'keys',
        'load',
        'loads',
        'update',
        'values'
    )
