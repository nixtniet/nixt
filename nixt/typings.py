# This file is placed in the Public Domain.


"default imports"


from collections.abc import Callable, Iterator
from types           import ModuleType, MappingProxyType
from typing          import Any, ClassVar, Dict, Generator, List, Set, TextIO
from typing          import Tuple, Union


def __dir__():
    return (
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


__all__ = __dir__()
