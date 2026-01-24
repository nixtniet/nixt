# This file is placed in the Public Domain.


"a clean namespace"


import types


class Reserved(Exception):

    pass


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
    "object contructor."
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


def edit(obj, setter={}, skip=False):
    "update object with dict."
    for key, val in items(setter):
        if skip and val == "":
            continue
        typed(obj, key, val)


def fqn(obj):
    "full qualified name."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def items(obj):
    "object's key,value pairs."
    if isinstance(obj, dict):
        return obj.items()
    if isinstance(obj, types.MappingProxyType):
        return obj.items()
    res = []
    for key in dir(obj):
        if key.startswith("_"):
            continue
        res.append((key, getattr(obj, key)))
    return sorted(res, key=lambda x: x[0])


def keys(obj):
    "object's keys."
    if isinstance(obj, dict):
        return obj.keys()
    if isinstance(obj, types.MappingProxyType):
        return obj.keys()
    if isinstance(obj, dict):
        return obj.keys()
    if isinstance(obj, type):
        res = []
        for key in dir(obj):
            if key.startswith("_"):
                continue
            res.append(key)
        return sorted(res)
    return obj.__dict__.keys()


def skip(obj, chars="_"):
    "skip keys containing chars."
    res = {}
    for key, value in items(obj):
        next = False
        for char in chars:
            if char in key:
                next = True
        if next:
            continue
        res[key] = value
    return res


def typed(obj, key, val):
    "assign proper types."
    try:
        setattr(obj, key, int(val))
        return
    except ValueError:
        pass
    try:
        setattr(obj, key, float(val))
        return
    except ValueError:
        pass
    if val in ["True", "true", True]:
        setattr(obj, key, True)
    elif val in ["False", "false", False]:
        setattr(obj, key, False)
    else:
        setattr(obj, key, val)


def update(obj, data, empty=True):
    "update object,"
    if isinstance(obj, type):
        for k, v in items(data):
            if k == "__dict__":
                continue
            if isinstance(getattr(obj, k, None), types.MethodType):
                raise Reserved(k)
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
    "object's values."
    if isinstance(obj, dict):
        return obj.values()
    res = []
    for key in sorted(dir(obj)):
        if key.startswith("_"):
            continue
        res.append(getattr(obj, key))
    return sorted(res)


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


"interface"


def __dir__():
    return (
        'Default',
        'Object',
        'construct',
        'edit',
        'fqn',
        'items',
        'keys',
        'skip',
        'typed',
        'update',
        'values'
    )
