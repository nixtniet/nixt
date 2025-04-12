# This file is placed in the Public Domain.


"a clean namespace"


from typing import Any


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


def construct(obj, *args, **kwargs) -> None:
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


def items(obj) -> [Any]:
    if isinstance(obj,type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> [str]:
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def update(obj, data) -> None:
    if not isinstance(data, type({})):
        obj.__dict__.update(vars(data))
    else:
        obj.__dict__.update(data)


def values(obj) -> [Any]:
    return obj.__dict__.values()


def __dir__():
    return (
        'Default',
        'Object',
        'construct',
        'items',
        'keys',
        'update',
        'values'
    )
