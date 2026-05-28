# This file is placed in the Public Domain.


"usefulness"


import inspect
import logging
import os
import pathlib


a = os.path.abspath
d = os.path.dirname
e = os.path.exists
i = os.path.isfile
j = os.path.join


class Utils:

    @staticmethod
    def cdir(path):
        "create directory."
        if e(path):
            return
        pth = pathlib.Path(path)
        if not e(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def check(path, md5s):
        "check for md5sums in a given path."
        ok = True
        if not e(path):
            return False
        for pth in os.listdir(path):
            if pth.startswith("__") or not pth.endswith(".py") or "statics" in pth:
                continue
            name = pth[:-3]
            modpath = j(path, pth)
            if Utils.md5(modpath) != md5s.get(name):
                logging.warning("mismatch %s", name)
                ok = False
        return ok

    @staticmethod
    def clsname(obj):
        "reutrn classname of an object."
        return obj.__class__.__name__

    @staticmethod
    def source(module):
        return module.__loader__.get_source(module.__name__)

    @staticmethod
    def html(text):
        "wrap text as html."
        return """<!doctype html>\n<html>   %s\n</html>""" % text

    @staticmethod
    def md5(path):
        "calculate md5sum of a file."
        import hashlib
        md5 = hashlib.md5()
        with open(path, "r", encoding="utf-8") as file:
            md5.update(file.read().encode("utf-8"))
        return str(md5.hexdigest())

    @staticmethod
    def md5dir(path, md5):
        "create a md5 for a directory."
        for fnm in os.listdir(path):
            if not fnm.endswith(".py"):
                continue
            mpath = j(path, fnm)
            with open(mpath, "r", encoding="utf-8") as file:
                md5.update(file.read().encode("utf-8"))

    @staticmethod
    def md5source(src):
        "determine md5 of source code."
        import hashlib
        md5 = hashlib.md5()
        md5.update(src.encode("utf-8"))
        return str(md5.hexdigest())

    @staticmethod
    def moddir():
        "return modules directory."
        return j(os.path.dirname(__spec__.loader.path), "modules")

    @staticmethod
    def modname(obj):
        "return package name of an object."
        return obj.__module__.split(".")[-1]

    @staticmethod
    def pkgname(obj):
        "return package name of an object."
        return obj.__module__.split(".", maxsplit=1)[0]

    @staticmethod
    def pipxdir(name):
        "return examples directory."
        return f"~/.local/share/pipx/venvs/{name}/share/{name}/"

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
    def where(obj):
        "path where object is defined."
        return os.path.dirname(inspect.getfile(obj))

    @staticmethod
    def wrapped(func):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func()
        except (KeyboardInterrupt, EOFError):
            pass


def __dir__():
    return (
        'LEVELS',
        'TIMES',
        'NoDate',
        'Format',
        'Log',
        'Time',
        'Utils',
        'a',
        'd',
        'e',
        'j'
    )
