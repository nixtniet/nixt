# This file is placed in the Public Domain.


"static tables"


import unittest


from nixt.statics import CORE, MODULES, NAMES


class TestStatics(unittest.TestCase):

    def test_core(self):
        self.assertTrue(CORE)

    def test_modules(self):
        self.assertFalse(MODULES)

    def test_names(self):
        self.assertFalse(NAMES)
