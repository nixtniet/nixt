# This file is placed in the Public Domain.


"object for an string"


class Broker:

    objects = {}

    @staticmethod
    def add(obj):
        Broker.objects[repr(obj)] = obj

    @staticmethod
    def all():
        return Broker.objects.values()

    @staticmethod
    def get(origin):
        return Broker.objects.get(origin, None)

    @staticmethod
    def like(origin):
        for orig in Broker.objects:
            if origin.split()[0] in orig.split()[0]:
                yield orig


def __dir__():
    return (
        'Broker',
   )
