# This file is placed in the Public Domain.


"an object for a string"


from .default import Any, ClassVar, Dict, Generator, Tuple


Anys    = Dict[str, Any]
Liked   = Generator[Tuple[str, Any], None, None]
Objects = Generator[Any, None, None]


class Broker:

    "map repr(obj) to obj"

    objects: ClassVar[Anys] = {}

    @classmethod
    def add(cls, obj: Any):
        "add object to the broker, key is repr(obj)."
        cls.objects[repr(obj)] = obj

    @classmethod
    def get(cls, origin: str) -> Any:
        "object by repr(obj)."
        return cls.objects.get(origin)

    @classmethod
    def has(cls, obj: Any) -> bool:
        "whether the Broker has object."
        return repr(obj) in cls.objects

    @classmethod
    def like(cls, text: str) -> Liked:
        "all keys with a substring in their key."
        for orig in cls.objects:
            if text in orig.split()[0]:
                yield (orig, cls.get(orig))

    @classmethod
    def objs(cls, attr: str) -> Objects:
        "objects with a certain attribute."
        for obj in cls.objects.values():
            if attr in dir(obj):
                yield obj

    @classmethod
    def remove(cls, obj: Any) -> None:
        "remove object."
        del cls.objects[repr(obj)]


def __dir__():
    return (
        'Broker',
    )
