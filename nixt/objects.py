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


class Dict:

    @staticmethod
    def construct(obj, *args, **kwargs):
        if args:
            val = args[0]
            if isinstance(val, zip):
                Dict.update(obj, dict(val))
            elif isinstance(val, dict):
                Dict.update(obj, val)
            else:
                Dict.update(obj, vars(val))
        if kwargs:
            Dict.update(obj, kwargs)

    @staticmethod
    def items(obj):
        if isinstance(obj, dict):
            return obj.items()
        if isinstance(obj, types.MappingProxyType):
            return obj.items()
        return obj.__dict__.items()

    @staticmethod
    def keys(obj):
        if isinstance(obj, dict):
            return obj.keys()
        return obj.__dict__.keys()

    @staticmethod
    def update(obj, data, empty=True):
        if isinstance(obj, type):
            for k, v in Dict.items(data):
                if isinstance(getattr(obj, k, None), types.MethodType):
                    raise Reserved(k)
                setattr(obj, k, v)
        elif isinstance(obj, dict):
            for k, v in Dict.items(data):
                setattr(obj, k, v)
        else:
            for key, value in Dict.items(data):
                if not empty and not value:
                    continue
                setattr(obj, key, value)

    @staticmethod
    def values(obj):
       if isinstance(obj, dict):
           return obj.values()
       res = []
       for key in dir(obj):
           if key.startswith("_"):
               continue
           res.append(getattr(obj, key))
       return res


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


def __dir__():
    return (
        'Default',
        'Dict',
        'Object',
        'Reserved'
    )
