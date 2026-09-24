# This file is placed in the Public Domain.


"usefullness"


import os
import pathlib
import uuid


from typing import List, Union
from types import ModuleType


class Utils:

    "useful functions"

    @staticmethod
    def cdir(path: str) -> None:
        "create directory."
        if os.path.exists(path):
            return
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clsname(obj: object) -> str:
        "return classname of an object."
        return obj.__class__.__name__

    @staticmethod
    def home(name: str) -> str:
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @staticmethod
    def listdir(path: str, ignore: str = "") -> List[str]:
        "list modules in a directory."
        return [
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(ignore)
               ]

    @staticmethod
    def shortid() -> str:
        "return a shortid."
        return str(uuid.uuid4())[:8]

    @staticmethod
    def source(module: ModuleType) -> Union[str, None]:
        "return the source of a module."
        if module.__spec__ is None:
            return
        if module.__spec__.loader is None:
            return
        get_source = getattr(module.__spec__.loader, "get_source")
        if get_source:
            return get_source(module.__name__)

    @staticmethod
    def spl(text: str, ignore: str = "") -> List[str]:
        "list from comma seperated string."
        try:
            ignores = ignore.split(",")
            result = text.split(",")
        except (TypeError, ValueError):
            result = []
        return [x for x in result if x and x not in ignores]

    @staticmethod
    def strip(path: str, nrchar: int = 3) -> str:
        "strip filename from path."
        return os.path.join(*path.split(os.sep)[-nrchar:])


def __dir__():
    return (
        'Time',
        'Utils'
    )
