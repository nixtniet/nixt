# This file is placed in the Public Domain.


"predefined"


from collections.abc import Callable
from types           import MappingProxyType, ModuleType
from typing          import Any, ClassVar, Dict, Generator, List
from typing          import Set, TextIO, Tuple, Union


Anys = Dict[str, Any]
Args = Union[List[str], None]
Callables = Dict[str, Callable]
Float = Union[float, None]
Floats = Dict[str, float]
Hash = Dict[str, str]
Integer = Union[int, None]
Items = List[Tuple[str, Any]]
Json = Union[dict,list,bool,float,int,str]
Keys = List[str]
Liked = Generator[Tuple[str, Any], None, None]
Module = Union[ModuleType, None]
Modules = Dict[str, ModuleType]
Objects = Generator[Any, None, None]
Paths = Generator[str, None, None]
Result = Generator[Tuple[str, Any], None, None]
Selector = Union[Dict[str, str], None]
Strings = Dict[str, str]
Values = List[Any]


def __dir__():
    return (
        'Any',
        'Anys',
        'Args',
        'Callable',
        'Callables',
        'ClassVar',
        'Dict',
        'Float',
        'Generator',
        'Hash',
        'Integer',
        'Items',
        'Json',
        'Keys',
        'Liked',
        'List',
        'MappingProxyType',
        'Module',
        'Modules',
        'ModuleType',
        'Objects',
        'Paths',
        'Result',
        'Selector',
        'Set',
        'Strings',
        'TextIO',
        'Union',
        'Values'
    )


__all__ = __dir__()
