# This file is placed in the Public Domain.


"an object for a string"


class Broker:

    objects = {}


def addobj(obj):
    "add object to the broker, key is repr(obj)."
    Broker.objects[repr(obj)] = obj


def getobj(origin):
    "object by repr(obj)."
    return Broker.objects.get(origin)


def getobjs(attr):
    "object with a certain attribute."
    for obj in Broker.objects.values():
        if attr in dir(obj):
            yield obj


def likeobj(txt):
    "all keys with a substring in their key."
    for orig in Broker.objects:
        if txt in orig.split()[0]:
            yield orig


def __dir__():
    return (
        'addobj',
        'getobj',
        'objs',
        'likeobj'
    )
