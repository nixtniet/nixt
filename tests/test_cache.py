# this file is placed in the Public Domain.


import unittest


from nixt.disk   import Cache
from nixt.object import Object


class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = Cache()
        self.cache.objs = {}

    def tearDown(self):
        self.cache.objs = {}

    def test_add(self):
        obj = Object()
        obj.a = "b"
        self.cache.add("bla", obj)
        oobj = self.cache.get("bla")
        self.assertEqual(oobj.a, "b")
