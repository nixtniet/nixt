# This file is placed in the Public Domain.


"usefulness"


import os
import uuid


from .default import Path


class Utils:

    "useful functions"

    @staticmethod
    def cdir(path):
        "create directory."
        if os.path.exists(path):
            return
        pth = Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clsname(obj):
        "return classname of an object."
        return obj.__class__.__name__

    @staticmethod
    def funcname(obj):
        "return functionname."
        try:
            return obj.__name__
        except AttributeError:
            return ""

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
    def shortid():
        "return a shortid."
        return str(uuid.uuid4())[:8]

    @staticmethod
    def source(module):
        "return the source of a module."
        if module.__spec__ is None:
            return None
        if module.__spec__.loader is None:
            return None
        get = getattr(module.__spec__.loader, "get_source", None)
        if get:
            return get(module.__name__)
        return None

    @staticmethod
    def spl(text, ignore=""):
        "list from comma seperated string."
        try:
            ignores = ignore.split(",")
            result = text.split(",")
        except (TypeError, ValueError):
            result = []
        return [x for x in result if x and x not in ignores]

    @staticmethod
    def strip(path, nrchar=3):
        "strip filename from path."
        return os.path.join(*path.split(os.sep)[-nrchar:])


def __dir__():
    return (
        'Utils',
    )
