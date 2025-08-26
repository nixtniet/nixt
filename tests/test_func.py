# This file is placed in the Public Domain.


"functions"


import unittest


from nixt.func   import edit, fmt, name
from nixt.object import Object


class TestFunctions(unittest.TestCase):

    def test_edit(self):
        obj = Object()
        edit(obj, {"a": "b"})
        self.assertEqual(obj.a, "b")
