# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.objects import Base, Method


class TestMethod(unittest.TestCase):

    def test_clear(self):
        obj = Base()
        obj.a = "b"
        Method.clear(obj)
        self.assertEqual(str(obj), "{}")
