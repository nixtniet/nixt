# This file is placed in the Public Domain.


"functions with an object as the first argument"


import datetime
import types


from .objects import Base, Object
from .utility import j


class Method:

    @staticmethod
    def clear(obj):
        "remove all items from the object."
        obj.__dict__.clear()

    @staticmethod
    def cls(obj):
        "return class name of an object."
        return Method.fqn(obj).split(".")[-1]

    @staticmethod
    def copy(obj):
        "return shallow copy of the object."
        oobj = type(obj)()
        Object.update(oobj, obj.__dict__.copy())
        return oobj

    @staticmethod
    def deleted(obj):
        "check whether obj had deleted flag set."
        return "__deleted__" in dir(obj) and obj.__deleted__

    @staticmethod
    def edit(obj, setter={}, skip=False):
        "update object with dict."
        for key, val in Object.items(setter):
            if skip and val == "":
                continue
            Method.typed(obj, key, val)

    @staticmethod
    def fmt(obj, args=[], skip=[], plain=False, empty=False):
        "format object info printable string."
        if args == []:
            args = list(obj.__dict__.keys())
        if args == []:
            args = [x for x in dir(obj) if not x.startswith("_")]
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
                txt += f"{key}={Method.cls(value)}({Method.fmt(value)}) "
        if txt == "":
            txt = "{}"
        return txt.strip()

    @staticmethod
    def fqn(obj):
        "full qualified name."
        kin = str(type(obj)).split()[-1][1:-2]
        if kin == "type":
            kin = f"{obj.__module__}.{obj.__name__}"
        return kin

    @staticmethod
    def fromkeys(obj, keyz, value=None):
        "create a new object with keys from iterable and values set to value/"
        return obj.__dict__.fromkeys(keyz, value)

    @staticmethod
    def get(obj, key, default=None):
        "return value for key if key is in the object, otherwise return default."
        return obj.__dict__.get(key, default)

    @staticmethod
    def ident(obj):
        "return ident string for object."
        return j(Method.fqn(obj), *str(datetime.datetime.now()).split())

    @staticmethod
    def merge(obj, obj2):
        "skip emoty values."
        for key, value in Object.items(obj2):
            if not value and getattr(obj, key, False):
                continue
            setattr(obj, key, value)

    @staticmethod
    def notset(obj, obj2):
        "only set if not set."
        for key, value in Object.items(obj2):
            if getattr(obj, key, False):
                continue
            if value:
                setattr(obj, key, value)

    @staticmethod
    def pop(obj, key, default=None):
        "remove key from object and return it's value. return default or KeyError."
        return obj.__dict__.pop(key, default)

    @staticmethod
    def popitem(obj):
        "remove and return (key, value) pair."
        return obj.__dict__.popitem()

    @staticmethod
    def reduce(obj):
        "return dict with values setted attributes."
        result = {}
        for key, value in Object.items(obj):
            if value:
                result[key] = value
        return result

    @staticmethod
    def search(obj, selector={}, matching=False):
        "check whether object matches search criteria."
        res = False
        for key, value in Object.items(selector):
            val = getattr(obj, key, None)
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

    @staticmethod
    def skip(obj, chars="_"):
        "skip keys containing chars."
        res = Base()
        for key, value in Object.items(obj):
            if isinstance(value, types.MethodType):
                continue
            donext = False
            for char in chars:
                if char in key:
                    donext = True
            if donext:
                continue
            setattr(res, key, value)
        return res

    @staticmethod
    def typed(obj, key, val):
        "assign proper types."
        if not val:
            return
        if val in ["True", "true", True]:
            return setattr(obj, key, True)
        if val in ["False", "false", False]:
            return setattr(obj, key, False)
        try:
            return setattr(obj, key, int(val))
        except ValueError:
            pass
        try:
            return setattr(obj, key, float(val))
        except ValueError:
            pass
        setattr(obj, key, val)


def __dir__():
    return (
        'Method',
    )
