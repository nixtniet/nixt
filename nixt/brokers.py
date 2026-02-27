# This file is placed in the Public Domain.


"an object for a string"


from .utility import Statics


class Broker(Statics):

    objects = {}

    def add(obj):
        "add object to the broker, key is repr(obj)."
        Broker.objects[repr(obj)] = obj

    def announce(txt):
        "announce text on all objects with an announce method."
        for obj in Broker.objs("announce"):
            obj.announce(txt)

    def get(origin):
        "object by repr(obj)."
        return Broker.objects.get(origin)

    def objs(attr):
        "objects with a certain attribute."
        for obj in Broker.objects.values():
            if attr in dir(obj):
                yield obj

    def has(obj):
        "whether the Broker has object."
        return repr(obj) in Broker.objects

    def like(txt):
        "all keys with a substring in their key."
        for orig in Broker.objects:
            if txt in orig.split()[0]:
                yield orig


def __dir__():
    return (
        'Broker',
    )
