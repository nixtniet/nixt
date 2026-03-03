# This file is placed in the Public Domain.


"an object for a string"


class Broker:

    objects = {}

    def announce(self, txt):
        "announce text on all objects with an announce method."
        for obj in self.objs("announce"):
            obj.announce(txt)

    def objs(self, attr):
        "objects with a certain attribute."
        for obj in self.objects.values():
            if attr in dir(obj):
                yield obj

    def has(self, obj):
        "whether the broker has object."
        return repr(obj) in self.objects

    def like(self, txt):
        "all keys with a substring in their key."
        for orig in self.objects:
            if txt in orig.split()[0]:
                yield orig

    def retrieve(self, origin):
        "object by repr(obj)."
        return self.objects.get(origin)

    def store(self, obj):
        "add object to the broker, key is repr(obj)."
        self.objects[repr(obj)] = obj


"interface"


def __dir__():
    return (
        'Broker',
    )
