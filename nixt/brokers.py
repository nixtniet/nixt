# This file is placed in the Public Domain.


"an object for a string."


import time


class Broker:

    objects = {}

    @classmethod
    def add(cls, obj):
        "add object to the broker, key is repr(obj)."
        cls.objects[repr(obj)] = obj

    @classmethod
    def get(cls, origin):
        "object by repr(obj)."
        return cls.objects.get(origin)

    @classmethod
    def has(cls, obj):
        "whether the Broker has object."
        return repr(obj) in cls.objects

    @classmethod
    def like(cls, txt):
        "all keys with a substring in their key."
        for orig in cls.objects:
            if txt in orig.split()[0]:
                yield orig, cls.get(orig)

    @classmethod
    def objs(cls, attr):
        "objects with a certain attribute."
        for obj in cls.objects.values():
            if attr in dir(obj):
                yield obj


class Clients:

    @staticmethod
    def announce(txt):
        "announce text on all objects with an announce method."
        for obj in Broker.objs("announce"):
            obj.announce(txt)

    @staticmethod
    def shutdown():
        "call stop on clients."
        for client in Broker.objs("wait"):
            client.wait()
        time.sleep(0.01)
        for client in Broker.objs("stop"):
            client.stop()
        time.sleep(0.01)


def __dir__():
    return (
        'Broker',
        'Clients'
    )
