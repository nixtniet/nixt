# This file is placed in the Public Domain.


"module md5sum"


import logging
import os


from typing import Dict


from .utility import Utils


logger = logging.getLogger(__name__)


class MD5:

    "module md5sums"

    @classmethod
    def check(cls, md5s: dict) -> bool:
        "check for md5sums in a given path."
        ok = True
        path = os.path.dirname(__spec__.origin)
        if not os.path.exists(path):
            return False
        for pth in os.listdir(path):
            if pth.startswith("__") or not pth.endswith(".py") or "statics" in pth:
                continue
            name = pth[:-3]
            modpath = os.path.join(path, pth)
            if md5s and cls.md5(modpath) != md5s.get(name):
                logger.warning("mismatch %s", name)
                ok = False
        return ok

    @classmethod
    def core(cls) -> str:
        "calculate md5 of the statics module."
        try:
            from . import statics
        except (ModuleNotFoundError, ImportError, SyntaxError):
            return ""
        return cls.source(Utils.source(statics))[:7].upper()

    @classmethod
    def createmd5(cls, path: str, data: Dict[str, str]) -> None:
        "create md5s for file in a directory."
        for pth in os.listdir(path):
            if pth.startswith("__") or not pth.endswith(".py") or "statics" in pth:
                continue
            name = pth[:-3]
            data[name] = cls.md5(os.path.join(path, pth))

    @classmethod
    def dir(cls, path: str, md5: Dict[str,str]) -> None:
        "create a md5 for a directory."
        for fnm in os.listdir(path):
            if not fnm.endswith(".py"):
                continue
            mpath = os.path.join(path, fnm)
            with open(mpath, "r", encoding="utf-8") as file:
                md5.update(file.read().encode("utf-8"))

    @classmethod
    def md5(cls, path: str) -> str:
        "calculate md5sum of a file."
        import hashlib
        md5 = hashlib.md5()
        with open(path, "r", encoding="utf-8") as file:
            md5.update(file.read().encode("utf-8"))
        return str(md5.hexdigest())

    @classmethod
    def source(cls, src: str) -> str:
        "determine md5 of source code."
        import hashlib
        md5 = hashlib.md5()
        md5.update(src.encode("utf-8"))
        return str(md5.hexdigest())


def __dir__():
    return (
        'MD5',
    )
