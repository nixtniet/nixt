# This file is placed in the Public Domain.


"default imports"


from collections.abc import Callable, Iterator
from types           import MethodType, ModuleType, MappingProxyType
from typing          import Any, ClassVar, Dict, List, Set, TextIO
from typing          import Tuple, Union, Generator


Anys = Dict[str, Any]
Hash = Dict[str, str]


__all__ = (
    'Any',
    'Anys',
    'Callable',
    'ClassVar',
    'Dict',
    'Generator',
    'Hash',
    'Iterator',
    'List',
    'MappingProxyType',
    'MethodType',
    'ModuleType',
    'Set',
    'TextIO',
    'Tuple',
    'Union'
)


def __dir__():
    return __all__
