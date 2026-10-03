# This file is placed in the Public Domain.


"predefined"


from collections.abc import Callable
from types           import MappingProxyType, ModuleType
from typing          import Any, ClassVar, Dict, Generator, List
from typing          import Set, TextIO, Tuple, Union


def __dir__():
    return (
        'Any',
        'Callable',
        'ClassVar',
        'Dict',
        'Generator',
        'List',
        'MappingProxyType',
        'ModuleType',
        'Set',
        'TextIO',
        'Tuple',
        'Union'
    )


__all__ = __dir__()
