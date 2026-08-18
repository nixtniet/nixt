# This file is placed in the Public Domain.


"usefulness"


import inspect
import os
import pathlib


class Utils:

    @classmethod
    def cdir(cls, path):
        "create directory."
        if os.path.exists(path):
            return
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clsname(obj):
        "return classname of an object."
        return obj.__class__.__name__

    @staticmethod
    def home(name):
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @staticmethod
    def listdir(path, ignore=""):
        "list modules in a directory."
        return [
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(ignore)
               ]

    @staticmethod
    def pipxdir(name):
        "return examples directory."
        return f"~/.local/share/pipx/venvs/{name}/share/{name}/"

    @staticmethod
    def skip(obj):
        "skip underscored keys."
        result = []
        for x in dir(obj):
            if x.startswith("_"):
                continue
            result.append(x)
        return sorted(result)

    @staticmethod
    def skipped(obj):
        "yield values without underscored keys."
        for key in dir(obj):
            if key.startswith("_"):
                continue
            yield getattr(obj, key)

    @staticmethod
    def source(module):
        "return the source of a module."
        return module.__loader__.get_source(module.__name__)

    @staticmethod
    def spl(txt, ignore=""):
        "list from comma seperated string."
        try:
            ignores = ignore.split(",")
            result = txt.split(",")
        except (TypeError, ValueError):
            result = []
        return [x for x in result if x and x not in ignores]

    @staticmethod
    def strip(path, nr=3):
        "strip filename from path."
        return os.path.join(*path.split(os.sep)[-nr:])

    @staticmethod
    def where(obj):
        "path where object is defined."
        return os.path.dirname(inspect.getfile(obj))


def __dir__():
    return (
        'Utils',
    )
