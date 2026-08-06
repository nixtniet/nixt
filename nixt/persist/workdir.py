# This file is placed in the Public Domain.


"persistence"


import os
import pathlib


class Workdir:

    wdr = ""

    @classmethod
    def configure(cls, name):
        cls.wdr = cls.wdr or Workdir.home(name)
        cls.skel()

    @classmethod
    def cdir(cls, path):
        "create directory."
        if os.path.exists(path):
            return
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def home(cls, name):
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @classmethod
    def kinds(cls):
        "show kind on objects in cache."
        if not cls.wdr:
            return []
        path = os.path.join(cls.wdr, "store")
        if not os.path.exists(path):
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
        return os.path.join(cls.wdr, "mods")

    @classmethod
    def pid(cls, name):
        "return path to pid file."
        if not cls.wdr:
            return
        filename = os.path.join(cls.wdr, f"{name}.pid")
        if os.path.exists(filename):
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
        if not os.path.exists(cls.wdr):
            cls.cdir(cls.wdr)
        path = os.path.abspath(cls.wdr)
        for wpth in ["config", "mods", "store"]:
            pth = pathlib.Path(os.path.join(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)


def __dir__():
    return (
        'Workdir',
    )
