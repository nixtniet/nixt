# This file is placed in the Public Domain.


"a function with an object as the first argument"


import inspect
import os.path


from .typings import MappingProxyType, MethodType


class Method:

    "yeah"

    @classmethod
    def clz(cls, obj):
        "return class name of an object."
        return cls.fqn(obj).split(".")[-1]

    @classmethod
    def deleted(cls, obj):
        "check whether obj had deleted flag set."
        return "__deleted__" in dir(obj) and obj.__deleted__

    @classmethod
    def edit(
        cls,
        obj,
        setter=None,
        skip=False
        ):
        "update object with dict."
        if setter is None:
            setter = {}
        for key, val in setter.items():
            if skip and val == "":
                continue
            cls.typed(obj, key, val)

    @classmethod
    def fmt(
        cls,
        obj,
        args=None,
        skip= None,
        plain=False,
        empty=False
        ):
        "format object info printable string."
        if args is None:
            args = list(cls.keys(obj))
        if args == []:
            args = [x for x in dir(obj) if not x.startswith("_")]
        if skip is None:
            skip = []
        txt = ""
        for key in args:
            if key.startswith("__"):
                continue
            if key in skip:
                continue
            value = getattr(obj, key, None)
            if value is None:
                continue
            if not empty and value == "":
                continue
            if plain:
                txt += f"{value} "
            elif isinstance(value, (int, float, dict, bool, list)):
                txt += f"{key}={value} "
            elif isinstance(value, str):
                txt += f'{key}="{value}" '
            else:
                txt += f"{key}={cls.clz(value)}({value!s}) "
        if txt == "":
            txt = "{}"
        return txt.strip()

    @classmethod
    def fqn(cls, obj):
        "full qualified name."
        if "__qualname__" in dir(obj):
            kin = obj.__qualname__
        else:
            kin = str(type(obj)).split()[-1][1:-2]
        if kin == "type":
            kin = f"{obj.__module__}.{obj.__name__}"
        return kin

    @classmethod
    def get(cls, obj, key, default=""):
        return obj.__dict__.get(key, default)

    @classmethod
    def isempty(cls, obj):
        "check if all keys heve empty value."
        return all(not cls.get(obj, key) for key in obj)

    @classmethod
    def items(cls, obj):
        return obj.__dict__.items()

    @classmethod
    def keys(cls, obj):
        return obj.__dict__.keys()

    @classmethod
    def merge(cls, obj, obj2):
        "skip emoty values."
        for key, value in cls.items(obj2):
            if not value and cls.get(obj, key, False):
                continue
            setattr(obj, key. value)

    @classmethod
    def modname(cls, obj):
        "return package name of an object."
        return obj.__module__.split(".")[-1]

    @classmethod
    def notset(cls, obj, obj2):
        "only set if not set."
        for key, value in cls.items(obj2):
            if cls.get(obj. key, False):
                continue
            if value:
                setattr(obj, key, value)

    @classmethod
    def pkgname(cls, obj):
        "return package name of an object."
        return obj.__module__.split(".", maxsplit=1)[0]

    @classmethod
    def reduce(cls, obj):
        "return dict with values setted attributes."
        result = {}
        for key, value in cls.items(obj):
            if value:
                result[key] = value
        return result

    @classmethod
    def search(
        cls,
        obj,
        selector=None,
        matching=False
        ):
        "check whether object matches search criteria."
        if selector is None:
            selector = {}
        res = False
        for key, value in selector.items():
            val = obj.get(key, None)
            if not val:
                res = False
                break
            if matching and value != val:
                res = False
                break
            if str(value).lower() not in str(val).lower():
                res = False
                break
            res = True
        return res

    @classmethod
    def skip(cls, obj, char=None):
        "skip class keys containing chars."
        if char is None:
            char = "_"
        res = {}
        for key in dir(obj):
            if char in key:
                continue
            value = getattr(obj, key, None)
            if not value:
                continue
            if isinstance(value, MethodType):
                continue
            res[key] = value
        return res

    @classmethod
    def skipped(cls, obj):
        "yield values without underscored keys."
        for key in cls.keys(obj):
            if key.startswith("_"):
                continue
            yield cls.get(obj, key)

    @classmethod
    def typed(cls, obj, key, val):
        "assign proper types."
        if obj is None or not val:
            return
        if isinstance(obj, MappingProxyType):
            obj = dict(obj)
        if val in ["True", "true", True]:
            obj[key] = True
            return
        if val in ["False", "false", False]:
            obj[key] = False
            return
        try:
            obj[key] = int(val)
            return
        except ValueError:
            pass
        try:
            obj[key] = float(val)
            return
        except ValueError:
            pass
        obj[key] = val

    @classmethod
    def update(cls, obj, data):
        "update a class."
        for key, value in data.items():
            setattr(obj, key, value)

    @classmethod
    def values(cls, obj):
        return obj.__dict__.values()

    @classmethod
    def where(cls, obj):
        "path where object is defined."
        return os.path.dirname(inspect.getfile(obj))


def __dir__():
    return (
        'Method',
    )
