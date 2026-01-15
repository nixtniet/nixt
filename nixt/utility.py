# This file is placed in the Public Domain.


"usefulness"


import datetime
import inspect
import os
import pathlib
import time


from .methods import fqn


def cdir(path):
    "create directory."
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def forever():
    "run forever until ctrl-c."
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def ident(obj):
    "return ident string for object."
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def md5sum(path):
    "return md5 of a file."
    import hashlib
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return hashlib.md5(txt, usedforsecurity=False).hexdigest()


def pkgname(obj):
    return obj.__module__.split(".")[0]


def pipxdir(name):
    "return examples directory."
    return f"~/.local/share/pipx/venvs/{name}/share/{name}/examples"


def spl(txt):
    "list from comma seperated string."
    try:
        result = txt.split(",")
    except (TypeError, ValueError):
        result = []
    return [x for x in result if x]


def where(obj):
    "path where object is defined."
    return os.path.dirname(inspect.getfile(obj))


def wrapped(func):
    "wrap function in a try/except, silence ctrl-c/ctrl-d."
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass


def __dir__():
    return (
        'cdir',
        'forever',
        'ident',
        'md5sum',
        'pipxdir',
        'pkgname',
        'spl',
        'where',
        'wrapped'
    )
