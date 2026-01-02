# This file is placed in the Public Domain.


"configuration"


from .objects import Default


class Config(Default):

    pass


def __dir__():
    return (
        'Config',
    )
