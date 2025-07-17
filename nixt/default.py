# This file is placed in the Public Domain.


"config"


from .object import Object


class Default(Object):

    def __getattr__(self, key):
        if key not in self:
            setattr(self, key, "")
        return self.__dict__.get(key, "")


"interface"


def __dir__():
    return (
        "Default",
    )
