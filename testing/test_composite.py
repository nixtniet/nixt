# This file is placed in the Public Domain.


import unittest


from nixt.objects import Object
from nixt.persist import Disk


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")

    def testcompositeprint(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        fnm = Disk.write(obj)
        ooo = Object()
        Disk.read(ooo, fnm)
        self.assertTrue(ooo.obj)
