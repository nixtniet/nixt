# This file is placed in the Public Domain.
# ruff: noqa: F403,F405


"interface"


import logging
import sys
import unittest


import nixt
import nixt.clients
import nixt.modules
import nixt.objects
import nixt.persist
import nixt.reactor
import nixt.storage
import nixt.threads


from nixt.objects import *


PACKAGE = [
    'clients',
    'modules',
    'objects',
    'persist',
    'reactor',
    'storage',
    'threads'
]


METHODS = [
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__len__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__'
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
