# This file is placed in the Public Domain.


"working directory"


import os
import pathlib


e = os.path.exists
j = os.path.join


class Workdir:

    wdr = ""

    @classmethod
    def home(cls, name):
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

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
    def moddir(cls):
        "return modules directory."
        return j(cls.wdr, "mods")

    @classmethod
    def pid(cls, name):
        "return path to pid file."
        if not cls.wdr:
            return
        filename = j(cls.wdr, f"{name}.pid")
        if e(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    @classmethod
    def skel(cls):
        "create directories."
        if not cls.wdr:
            return
        if not e(cls.wdr):
            Disk.cdir(cls.wdr)
        path = os.path.abspath(cls.wdr)
        for wpth in ["config", "logs", "mods", "store"]:
            pth = pathlib.Path(j(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)


def __dir__():
    return (
        'Workdir',
    )
