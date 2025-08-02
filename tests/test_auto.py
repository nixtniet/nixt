# This file is placed in the Public Domain.


"method tests"


import unittest


from nixt.auto   import Auto
from nixt.method import edit


class TestMethods(unittest.TestCase):

    def test_auto(self):
        obj = Auto()
        obj.a = "b"
        edit(obj, {"a": "c"})
        self.assertEqual(obj.a, "c")
