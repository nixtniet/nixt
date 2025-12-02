# This file is placed in the Public Domain.

"""an object for a string

The repr() of an object is used a a string to retrieve the object from the broker.

examples:

>>> from nixt.brokers import Broker
>>> b = Broker()
>>> from nixt.objects import Object
>>> o = Object()
>>> b.add(o)
>>> oo = b.get(repr(o))
>>> o == oo
True

"""


class Broker:

    objects = {}

    @staticmethod
    def add(obj):
        Broker.objects[repr(obj)] = obj
        
    @staticmethod
    def all(attr):
        for obj in Broker.objects.values():
            if attr in dir(obj):
                yield obj

    @staticmethod
    def get(origin):
        return Broker.objects.get(origin)

    @staticmethod
    def like(txt):
        for orig in Broker.objects:
            if origin.split()[0] in orig.split()[0]:
                yield orig


def display(evt):
    bot = Broker.get(evt.orig)
    bot.display(evt)


def __dir__():
    return (
        'Broker',
        'display'
    )
