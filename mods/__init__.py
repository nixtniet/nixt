# This file is placed in the Public Domain.
# ruff: noqa: F401


"interface"


import importlib
import os
import time


IGNORE    = ["llm.py", "mbx.py", "web.py", "wsd.py", "udp.py"]
NAME      = os.path.dirname(__file__).split(os.sep)[-1]
MODS      = sorted([
                    x[:-3] for x in os.listdir(os.path.dirname(__file__))
                    if x.endswith(".py") and not x.startswith("__")
                    and x not in IGNORE
                   ])
STARTTIME = time.time()


for name in MODS:
    mname = f"{NAME}.{name}"
    importlib.import_module(mname, NAME)


def __dir__():
    return MODS
