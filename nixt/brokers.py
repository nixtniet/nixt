# This file is placed in the Public Domain.


"an object for a string"


from typing import ClassVar, Dict, Generator, Tuple


class Broker:

    "map repr(obj) to obj"

    objects: ClassVar[Dict[str, object]] = {}

    @classmethod
    def add(cls, obj) -> str:
        "add object to the broker, key is repr(obj)."
        oid = repr(obj)
        cls.objects[oid] = obj
        return oid

    @classmethod
    def get(cls, origin) -> object:
        "object by repr(obj)."
        return cls.objects.get(origin)

    @classmethod
    def has(cls, obj) -> bool:
        "whether the Broker has object."
        return repr(obj) in cls.objects

    @classmethod
    def like(cls, txt) -> Generator[Tuple[str, object], None, None]:
        "all keys with a substring in their key."
        for orig in cls.objects:
            if txt in orig.split()[0]:
                yield orig, cls.get(orig)

    @classmethod
    def objs(cls, attr) -> Generator[object, None, None]:
        "objects with a certain attribute."
        for obj in cls.objects.values():
            if attr in dir(obj):
                yield obj

    @classmethod
    def remove(cls, obj) -> None:
        del cls.objects[repr(obj)]


def __dir__():
    return (
        'Broker',
    )
