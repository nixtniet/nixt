# This file is placed in the Public Domain.


"find"


import unittest


from nixt.objects import Object
from nixt.persist import Workdir, find, getpath, write


class TestFind(unittest.TestCase):

    def setUp(self):
        Workdir.wdr = ".test"

    def test_find(self):
        obj = Object()
        write(obj, getpath(obj))
        result = list(find("nixt.object.Object"))
        self.assertNotEqual(len(result), 0)
