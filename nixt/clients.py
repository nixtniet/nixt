# This file is placed in the Public Domain.


"handling client events"


from .display import Display, Output
from .handler import Engine


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


class Buffer(Engine, Output):

    "buffered output"

    def __init__(self):
        Engine.__init__(self)
        Output.__init__(self)
        Broker.add(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, **kwargs):
        "start output loop."
        Engine.start(self, **kwargs)
        Output.start(self, **kwargs)

    def stop(self):
        "stop output loop."
        Engine.stop(self)
        Output.stop(self)


class Client(Engine, Display):

    "display with coupled handler"

    def __init__(self):
        Engine.__init__(self)
        Display.__init__(self)
        Broker.add(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


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
        'Buffer',
        'Client',
        'Clients'
    )
