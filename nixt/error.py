# This file is placed in the Public Domain.


"list of errors"


import traceback


class Errors:

    name = __file__.rsplit("/", maxsplit=2)[-2]
    errors = []
   
    
def full(exc) -> str:
    return traceback.format_exception(type(exc),exc,exc.__traceback__)


def later(exc) -> None:
    Errors.errors.append(exc)


def __dir__():
    (
     'Errors',
     'full',
     'later'
    )
