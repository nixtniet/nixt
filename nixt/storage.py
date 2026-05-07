# This file is placed in the Public Domain.


"disk"


import json
import logging
import os
import threading


from .encoder import Json
from .methods import Method
from .objects import Object
from .persist import Cache
from .workdir import Workdir
from .utility import Utils


e = os.path.exists
j = os.path.join


class Disk:

    lock = threading.RLock()

    @classmethod
    def read(cls, obj, path, base="store", error=True):
        "read object from path."
        with cls.lock:
            pth = j(Workdir.wdr, base, path)
            if not e(pth):
                return False
            with open(pth, "r", encoding="utf-8") as fpt:
                try:
                    Object.update(obj, Json.load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    logging.error("failed read at %s: %s", pth, str(ex))
                    if error:
                        raise
                    return False
            return True

    @classmethod
    def write(cls, obj, path="", base="store", skip=False):
        "write object to disk."
        with cls.lock:
            if path == "":
                path = Method.ident(obj)
            pth = j(Workdir.wdr, base, path)
            if not e(pth):
                Workdir.skel()
            Utils.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                Json.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


def __dir__():
    return (
        'Disk',
    )
