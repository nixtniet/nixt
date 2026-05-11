# This file is placed in the Public Domain.


"a clean namespace"


import datetime
import types


from .utility import j


class Base:

    def __init__(self, *args, **kwargs):
        Object.construct(self, *args, **kwargs)

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


class Object:


    @staticmethod
    def construct(obj, *args, **kwargs):
        "object contructor."
        if args:
            val = args[0]
            if isinstance(val, zip):
                Object.update(obj, dict(val))
            elif isinstance(val, dict):
                Object.update(obj, val)
            else:
                Object.update(obj, vars(val))
        if kwargs:
            Object.update(obj, kwargs)

    @staticmethod
    def items(obj):
        "object's key,value pairs."
        if isinstance(obj, type):
            return [(x, getattr(obj, x)) for x in dir(obj) if not x.startswith("_")]
        if isinstance(obj, dict):
            return obj.items()
        if isinstance(obj, types.MappingProxyType):
            return obj.items()
        return obj.__dict__.items()

    @staticmethod
    def keys(obj):
        "object's keys."
        if isinstance(obj, dict):
            return obj.keys()
        if isinstance(obj, types.MappingProxyType):
            return obj.keys()
        return obj.__dict__.keys()

    @staticmethod
    def update(obj, data, empty=True):
        "update object,"
        if isinstance(obj, type):
            if isinstance(data, type):
                for key in dir(data):
                    if '_' in key:
                        continue
                    value = getattr(data, key, None)
                    if value:
                        setattr(obj, key, value)
            else:
                for key, value in Object.items(data):
                    setattr(obj, key, value)
        elif isinstance(obj, dict):
            if isinstance(data, dict):
                obj.update(data)
            else:
                obj.update(data.__dict__)
        elif isinstance(obj.__dict__, types.MappingProxyType):
            for key, value in data.items():
                setattr(obj, key, value)
        elif isinstance(data, dict):
            obj.__dict__.update(data)
        else:
            obj.__dict__.update(data.__dict__)

    @staticmethod
    def values(obj):
        "object's values."
        if isinstance(obj, type):
            return [getattr(obj, x) for x in dir(obj) if not x.startswith("_")]
        if isinstance(obj, dict):
            return obj.values()
        if isinstance(obj.__dict__, types.MappingProxyType):
            res = []
            for key in obj.__dict__:
                res.append(obj[key])
            return res
        return obj.__dict__.values()


class Set:

    @staticmethod
    def clear(obj):
       "remove all elements."
       obj.__dict__.clear()

    @staticmethod
    def copy(obj):
        "return a shallow copy."
        oobj = type(obj)()
        Object.update(oobj, obj.__dict__.copy())
        return oobj

    @staticmethod
    def difference(obj, *others):
        "return a new object with elements that are not in the others."
            
    @staticmethod
    def difference_update(obj, *others):
        "update the object, removing elements found in others."

    @staticmethod
    def discard(obj):
        "remove an element from a object if it is a member."

    @staticmethod
    def intersection(obj, *others):
        "return a new object with elements common to all others."

    @staticmethod
    def intersection_update(obj, *others):
        "update the object, keeping only elements found in it and all others."

    @staticmethod
    def isdisjoint(obj, other):
        "return True if two objects have a null intersection."

    @staticmethod
    def isubset(obj, other):
        "report whether another object contains this object's keys."

    @staticmethod
    def isuperset(obj, other):
        "report whether this object contains another object's keys."

    @staticmethod
    def pop(obj):
        "remove and return an arbitrary object's element."
        return obj.__dict__.pop(key, default)

    @staticmethod
    def remove(obj, other):
        "remove an element from an object."
         
    @staticmethod
    def symmetric_difference(obj, other):
        "return a new  object with elements in either the object or other but not both."
    
    @staticmethod
    def symmetric_difference_update(obj, other):
        "update the object, keeping only elements found in either object, but not in both."

    @staticmethod
    def union(obj, *others):
        "return a new object with elements from the object and all others."

    @staticmethod
    def update(obj, *others):
        "update the set, adding elements from all others."


def __dir__():
    return (
        'Base',
        'Object',
        'Set'
    )
