# This file is placed in the Public Domain.
# ruff: noqa: F403,F405


"interface"


import logging
import sys
import unittest


import nixt
import nixt.client
import nixt.cmnd
import nixt.disk
import nixt.engine
import nixt.event
import nixt.find
import nixt.fleet
import nixt.log
import nixt.method
import nixt.object
import nixt.output
import nixt.paths
import nixt.thread
import nixt.timer
import nixt.utils


from nixt.object import *


PACKAGE = [
    "client",
    "cmnd",
    "disk",
    "engine",
    "event",
    "find",
    "fleet",
    "log",
    'method',
    "object",
    'output',
    "paths",
    "thread",
    "timer",
    "utils"
]


METHODS = [
    "__class__",
    "__delattr__",
    "__dict__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getstate__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__le__",
    "__len__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "__weakref__",
]


class TestInterface(unittest.TestCase):
    def test_package(self):
        okd = True
        for mod in PACKAGE:
            mod1 = getattr(nixt, mod, None)
            if not mod1:
                okd = False
                print(mod)
                break
        self.assertTrue(okd)

    def test_objects(self):
        okd = True
        obj = Object()
        dirr = dir(obj)
        for meth in METHODS:
            if meth not in dirr:
                okd = False
                print(f"{meth} not found")
        self.assertTrue(okd)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("SomeTest.testSomething").setLevel(logging.DEBUG)
    unittest.main()
