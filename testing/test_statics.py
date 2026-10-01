# This file is placed in the Public Domain.


"static tables"


import unittest


from nixt.statics import CORE, MODULES, NAMES


class TestStatics(unittest.TestCase):

    "statics unittests"

    def test_core(self):
        "test for core definitions."
        self.assertTrue(CORE)

    def test_modules(self):
        "test for modules emptyness."
        self.assertFalse(MODULES)

    def test_names(self):
        "test for names emptyness."
        self.assertFalse(NAMES)
