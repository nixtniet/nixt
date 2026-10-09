# This file is placed in the Public Domain.


"default imports"


from collections.abc import Callable, Iterator
from types           import ModuleType, MappingProxyType
from typing          import Any, ClassVar, Dict, List, Set, TextIO
from typing          import Tuple, Union, Generator


__all__ = (
    'Any',
    'Callable',
    'ClassVar',
    'Dict',
    'Generator',
    'Iterator',
    'List',
    'MappingProxyType',
    'ModuleType',
    'Set',
    'TextIO',
    'Tuple',
    'Union'
)


def __dir__():
    return __all__
