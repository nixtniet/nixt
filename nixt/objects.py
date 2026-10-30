# This file is placed in the Public Domain.


"a clean namespace"


class Object:

    "inheritence without the methods"

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


class Data(Object):

    "defaulting to string"

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            Dict.update(self, args[0])
        if kwargs:
            Dict.update(self, kwargs)

    def __getattr__(self, key):
        if key in dir(self):
            return self.__getattribute__(key)
        return ""


class Dict:

    "dictionary like operations on an object"

    @classmethod
    def get(cls, obj, key, default=""):
        "get attribute from object."
        return obj.__dict__.get(key, default)

    @classmethod
    def items(cls, obj):
        "return items on object."
        return obj.__dict__.items()

    @classmethod
    def keys(cls, obj):
        "return keys from object."
        return obj.__dict__.keys()

    @classmethod
    def merge(cls, obj, obj2):
        "skip emoty values."
        for key, value in cls.items(obj2):
            if not value and cls.get(obj, key, False):
                continue
            setattr(obj, key, value)

    @classmethod
    def update(cls, obj, data):
        "update an object."
        for key, value in data.items():
            setattr(obj, key, value)

    @classmethod
    def values(cls, obj):
        "fetch values from object."
        return obj.__dict__.values()


def __dir__():
    return (
        'Data',
        'Dict',
        'Object'
    )
