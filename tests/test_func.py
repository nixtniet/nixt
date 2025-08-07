# This file is placed in the Public Domain.


"method tests"


import unittest


from nixt.func   import edit
from nixt.object import Object


class TestMethods(unittest.TestCase):

    def test_edit(self):
        obj = Object()
        obj.a = "b"
        edit(obj, {"a": "c"})
        self.assertEqual(obj.a, "c")
