 # This file is placed in the Public Domain.


"an object for a string"


class Broker:

    "map repr(obj) to obj"

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
    def like(cls, text):
        "all keys with a substring in their key."
        for orig in cls.objects:
            if text in orig.split()[0]:
                yield (orig, cls.get(orig))

    @classmethod
    def objs(cls, attr):
        "objects with a certain attribute."
        for obj in cls.objects.values():
            if attr in dir(obj):
                yield obj

    @classmethod
    def remove(cls, obj):
        "remove object."
        del cls.objects[repr(obj)]


class Clients:

    "collection of clients"

    @staticmethod
    def announce(text):
        "announce text on all clients."
        for obj in Broker.objs("announce"):
            obj.announce(text)

    @staticmethod
    def display(msg):
        "display results."
        bot = Broker.get(msg.orig)
        if bot:
            bot.display(msg)


def __dir__():
    return (
        'Broker',
        'Clients'
    )
