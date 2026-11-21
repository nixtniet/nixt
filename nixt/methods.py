# This file is placed in the Public Domain.


"a function with an object/dict as the first argument"


import inspect
import os.path


from .functio import Dicts


class Methods:

    "methods"

    @classmethod
    def clsname(cls, obj):
        "class name of an object."
        if isinstance(obj, type):
            return obj.__name__
        if "__self__" in dir(obj):
            return obj.__self__.__class__.__name__
        return obj.__class__.__name__

    @classmethod
    def clz(cls, obj):
        "return class name of an object."
        return cls.fqn(obj).split(".")[-1]

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
    def funcname(cls, obj):
        "return functionname."
        try:
            return obj.__name__
        except AttributeError:
            return ""

    @classmethod
    def getname(cls, obj):
        "string of function/method."
        if inspect.ismethod(obj):
            return f"{cls.clsname(obj)}.{obj.__name__}"
        if inspect.isfunction(obj):
            return repr(obj).split()[1]
        return repr(obj)

    @classmethod
    def modname(cls, obj):
        "return package name of an object."
        return obj.__module__.split(".")[-1]

    @classmethod
    def pkgname(cls, obj):
        "return package name of an object."
        return obj.__module__.split(".", maxsplit=1)[0]

    @classmethod
    def skip(cls, obj, char=None):
        "return values with keys don't contain an underscore."
        return Dicts.skip(vars(obj), char)

    @classmethod
    def todict(cls, obj):
        "convert object to dictionary."
        res = {}
        for key in dir(obj):
            if key.startswith("_"):
                continue
            res[key] = getattr(obj, key)
        return res

    @classmethod
    def typed(cls, obj, key, value):
        "set typed values on the object."
        try:
            obj = vars(obj)
        except TypeError:
            pass
        Dicts.typed(obj, key, value)

    @classmethod
    def update(cls, obj, data):
        "update object with a dict."
        for key, value in data.items():
            setattr(obj, key, value)

    @classmethod
    def where(cls, obj):
        "path where object is defined."
        return os.path.dirname(inspect.getfile(obj))


def __dir__():
    return (
        'Methods',
    )
