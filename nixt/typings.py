# This file is placed in the Public Domain.


"predefined"


from collections.abc import Callable
from typing          import Any, Generator, Set, TextIO, Tuple
from typing          import ClassVar, Dict, List, Union
from types           import ModuleType


Anys = Dict[str, Any]
Args = Union[List[str], None]
Commands = Dict[str, Callable]
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
Times = List[str]
Todo = Dict[str, List[Any]]
Values = List[Any]


def __dir__():
    return (
        'Any',
        'Anys',
        'Args',
        'Callable',
        'ClassVar',
        'Commands',
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
        'Times',
        'Todo',
        'Union',
        'Values'
    )
