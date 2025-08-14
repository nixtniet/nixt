# This file is placed in the Public Domain.


"md5sums"


import hashlib
import importlib
import importlib.util
import os


from .pkg import load


checksum = "ec2e91056cc56049af4546de374179d7"
checksum = ""


path = os.path.dirname(__file__)
path = os.path.join(path, "modules")
pname = f"{__package__}.modules"


def check(name, hash=""):
    mname = f"{pname}.{name}"
    pth = os.path.join(path, name + ".py")
    spec = importlib.util.spec_from_file_location(mname, pth)
    if not spec:
        return False
    if md5sum(pth) == (hash or MD5.get(name, None)):
        return True
    if Main.md5:
        rlog("error", f"{name} failed md5sum check")
    return False


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return str(hashlib.md5(txt).hexdigest())


def table():
    pth = os.path.join(path, "tbl.py")
    if os.path.exists(pth) and (not checksum or (md5sum(pth) == checksum)):
        return load("tbl")
    return {}
