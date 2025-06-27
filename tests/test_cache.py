# This file is placed in the Public Domain.


import unittest
import time
import os


from nixt.cache import Cache, find, fntime, isdeleted, last, search, read, write
from nixt.object import Object, fqn


class TestCache(unittest.TestCase):

    def setUp(self):
        Cache.names = []
        Cache.objs = {}

    def tearDown(self):
        Cache.names = []
        Cache.objs = {}

    def test_add_and_get(self):
        pass

    def test_update(self):
        pass

    def test_typed(self):
        pass

    def test_long(self):
        pass


class TestCacheFunctions(unittest.TestCase):

    def setUp(self):
        Cache.names = []
        Cache.objs = {}

    def tearDown(self):
        Cache.names = []
        Cache.objs = {}

    def test_find(self):
        pass

    def test_fntime(self):
        pass

    def test_isdeleted(self):
        pass

    def test_last(self):
        pass

    def test_search(self):
        pass

    def test_read_and_write(self):
        pass
        

if __name__ == "__main__":
    unittest.main()
