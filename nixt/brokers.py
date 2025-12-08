# This file is placed in the Public Domain.


"an object for a string"


class Broker:

    objects = {}


def addobj(obj):
    Broker.objects[repr(obj)] = obj
        

def all(attr):
    for obj in Broker.objects.values():
       if attr in dir(obj):
           yield obj


def getobj(origin):
    return Broker.objects.get(origin)


def like(txt):
    for orig in Broker.objects:
        if orig.split()[0] in orig.split()[0]:
            yield orig


def display(evt):
    bot = getobj(evt.orig)
    bot.display(evt)


def __dir__():
    return (
        'Broker',
        'addobj',
        'all',
        'display',
        'getobj',
        'like'
    )
