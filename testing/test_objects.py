# This file is placed in the Public Domain.


"obejcts tests"


import unittest


from nixt.defines import Data, Object


class TestData(unittest.TestCase):

    def construct(self):
        data = Data()
        self.assertTrue(type(data), Data)


class TestObject(unittest.TestCase):

    def construct(self):
        obj = Object()
        self.assertTrue(type(obj), Object)


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")
