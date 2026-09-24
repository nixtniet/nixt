# This file is placed in the Public Domain.


"module management"


import logging
import os


from types  import ModuleType
from typing import ClassVar, Dict, List, Union


from .methods import Method
from .sources import MD5
from .utility import Utils


logger = logging.getLogger(__name__)


class Mods:

    "modules"

    core: ClassVar[Dict[str, str]] = {}
    dirs: ClassVar[Dict[str, str]] = {}
    md5s: ClassVar[Dict[str, str]] = {}
    mods: ClassVar[Dict[str, ModuleType]] = {}

    @classmethod
    def dir(cls, pkgname: str, path: str) -> None:
        "add module/path."
        cls.dirs[pkgname] = path

    @classmethod
    def get(cls, name: str, force: bool = False) -> Union[ModuleType, None]:
        "return module from cache or import module."
        for pkgname, path in cls.dirs.items():
            modname = f"{pkgname}.{name}"
            mod = cls.mods.get(modname, None)
            if mod:
                return mod
            fnm = os.path.join(path, name + ".py")
            if not os.path.exists(fnm):
                continue
            if not force and cls.md5s:
                md5 = MD5.md5(fnm)
                md5s = cls.md5s.get(name)
                if md5s and md5 != md5s:
                    logger.warning("mismatch %s", modname)
            return cls.importer(modname, fnm)
        return None

    @classmethod
    def has(cls, attr: str) -> str:
        "return comma seperated string of module names containing an attribute."
        result = []
        for modname in cls.list():
            mod = cls.get(modname)
            if not mod:
                continue
            if not getattr(mod, attr, False):
                continue
            result.append(mod.__name__.split(".")[-1])
        return ",".join(result)

    @classmethod
    def importer(cls, name: str, pth: str = "") -> Union[ModuleType, None]:
        "import module by path."
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, pth)
        if not spec or not spec.loader:
            return None
        cls.mods[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mods[name])
        return cls.mods[name]

    @classmethod
    def list(cls) -> List[str]:
        "comma seperated list of available modules."
        mods = []
        for path in cls.dirs.values():
            if not os.path.exists(path):
                continue
            mods.extend(Utils.listdir(path))
        return sorted(set(mods))

    @classmethod
    def minimal(cls) -> str:
        "return package minimal path."
        return os.path.join(Method.where(Mods), "minimal")

    @classmethod
    def moddir(cls) -> str:
        "return package modules path."
        return os.path.join(Method.where(Mods), "modules")

    @classmethod
    def statics(cls) -> None:
        "read table,"
        try:
            from .statics import CORE
            cls.core.update(CORE)
        except (ImportError, SyntaxError, ValueError):
            pass
        try:
            from .statics import MODULES
            cls.md5s.update(MODULES)
        except (ImportError, SyntaxError, ValueError):
            pass

    @classmethod
    def table(cls) -> None:
        "read static tables."
        cls.statics()
        if cls.core:
            MD5.check(cls.core)


def __dir__():
    return (
        'Mods',
    )
