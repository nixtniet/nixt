# this file is placed in the Public Domain.


from threading import RLock
from types     import ModuleType
from typing    import Any, Callable, Dict


from ..event  import Event
from ..object import Object
from ..thread import Thread


lock: RLock
path: str


CHECKSUM : str
MD5:       Dict[str, str]
NAMEs:     Dict[str, str]


class Default(Object):

    def __getattr__(self, key: str) -> str: ...


class Main(Default):

    debug:   bool
    gets :   Default
    ignore:  str
    init:    str
    md5:     bool
    name:    str
    opts:    Default
    otxt:    str
    sets:    Default
    verbose: bool
    version: int


def check(name: str, md5: str="") -> bool: ...
def getmod(name: str) -> ModuleType: ...
def gettbl(name: str) -> Dict[str, str]: ...
def load(name: str) -> ModuleType: ...
def md5sum(modpath: str) -> str: ...
def mods(names: str="") -> list[ModuleType]: ...
def modules(mdir: str="") -> list[str]: ...
def setdebug(module: ModuleType) -> None: ...
def table() -> Dict[str, str]: ...


class Commands:

    cmds: Dict[str, Callable]
    md5: Dict[str, str]
    names: Dict[str, str]

    @staticmethod
    def add(func: Callable, mod: str="") -> None: ...

    @staticmethod
    def get(cmd: str) -> Callable: ...


def command(evt: Event) -> None: ...
def inits(names: list[str]) -> list[tuple[ModuleType, Thread]]: ...
def parse(obj: Object, txt: str="") -> None: ...
def scan(mod: ModuleType) -> None: ...
def settable() -> None: ...


def debug(*args: list[Any]): ...
def elapsed(seconds: float, short: bool=True) -> str: ...
def spl(txt: str) -> list[str]: ...


def edit(obj: Object, setter: Dict[str, str], skip: bool=False) -> None: ...
def fmt(obj: Object, args: list=[], skip: bool=False, plain: bool=False) -> None: ...


def __dir__() -> list[str]: ...
