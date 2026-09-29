# This file is placed in the Public Domain.


"predefined"


from collections.abc import Callable
from types           import ModuleType
from typing          import Any, ClassVar, Dict, Generator, List
from typing          import Set, TextIO, Tuple, Union


Anys = Dict[str, Any]
Args = Union[List[str], None]
Callables = Dict[str, Callable]
Final = Union[Callable, None]
Float = Union[float, None]
Hash = Dict[str, str]
Items = List[Tuple[str, Any]]
Json = Union[dict,list,bool,float,int,str]
Keys = List[str]
Liked = Generator[Tuple[str, Any], None, None]
Objects = Generator[Any, None, None]
Paths = Generator[str, None, None]
Result = Generator[Tuple[str, Any], None, None]
Selector = Union[Dict[str, str], None]
Skipped = Generator[Any, None, None]
TimeOut = Union[float, None]
Times = Tuple[str]
Todo = Dict[str, List[Any]]
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
        'Final',
        'Generator',
        'Hash',
        'Items',
        'Json',
        'Keys',
        'Liked',
        'List',
        'ModuleType',
        'Objects',
        'Paths',
        'Result',
        'Selector',
        'Set',
        'Skipped',
        'TextIO',
        'TimeOut',
        'Todo',
        'Union',
        'Values'
    )


__all__ = __dir__()
