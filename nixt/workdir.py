# This file is placed in the Public Domain.


"persistence through storage"


import os
import pathlib


from .utility import Utils


e = os.path.exists
j = os.path.join


class Workdir:

    wdr = ""

    @classmethod
    def kinds(cls):
        "show kind on objects in cache."
        path = j(cls.wdr, "store")
        if not e(path):
            cls.skel()
        return os.listdir(path)

    @classmethod
    def long(cls, name):
        "expand to fqn."
        if "." in name:
            return name
        split = name.split(".")[-1].lower()
        res = name
        for names in cls.kinds():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @classmethod
    def skel(cls):
        "create directories."
        if not cls.wdr:
            return
        if not e(cls.wdr):
            Utils.cdir(cls.wdr)
        path = os.path.abspath(cls.wdr)
        for wpth in ["config", "mods", "store"]:
            pth = pathlib.Path(j(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)

    @classmethod
    def workdir(cls, path=""):
        "return workdir."
        return j(cls.wdr, path)


def __dir__():
    return (
        'Workdir',
    )
