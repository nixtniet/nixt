# This file is placed in the Public Domain.


"method tests"


import unittest


from nixt.modules import Auto


class TestMethods(unittest.TestCase):

    def test_auto(self):
        obj = Auto()
        obj.a = "b"
        self.assertEqual(obj.a, "b")
