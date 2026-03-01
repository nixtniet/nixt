# This file is placed in the Public Domain.


import os
import shutil
import sys
import unittest


sys.path.insert(0, ".")


from nixt.persist import *
from nixt.persist import cache
from nixt.objects import Object


Main.wdr = '.test'


class TestCache(unittest.TestCase):

    def test_add(self):
        obj = Object()
        cache.add("test", obj)
        self.assertTrue("test" in cache.paths)
    
    def test_get(self):
        obj = Object()
        cache.add("test", obj)
        oobj = cache.get("test")
        self.assertTrue(obj is oobj)

    def test_sync(self):
        obj = Object()
        cache.add("test", obj)
        cache.sync("test", {"a": "b"})     
        self.assertEqual(getattr(cache.get("test"), "a"), "b") 


class TestLocate(unittest.TestCase):

    def test_attrs(self):
        obj = Object()
        obj.a = "b"
        write(obj)
        self.assertTrue("a" in attrs(fqn(obj)))

    def test_count(self):
        obj = Object()
        obj.a = "b"
        shutil.rmtree(".test")
        write(obj)
        self.assertTrue(count(fqn(Object)) == 1)

    def test_find(self):
        obj = Object()
        obj.a = "b"
        result = list(find(fqn(obj), {"a": "b"}))
        self.assertTrue(len(result) == 1)

    def fns(self):
        obj = Object()
        filenames = fns(fqn(obj))
        self.assertTrue(filenames)


class TestWorkdir(unittest.TestCase):

    def cdir(self):
        pass

    def kinds(self):
        pass

    def long(self):
        pass
    
    def pidfile(self):
        pass

    def skel(self):
        pass

    def setwd(self):
        pass

    def strip(self):
        pass

    def workdir(self):
        pass


class TestPersist(unittest.TestCase):

    def test_first(self):
        pass

    def test_last(self):
        pass

    def test_read(self):
        pass

    def test_write(self):
        obj = Object()
        opath = write(obj)
        self.assertTrue(os.path.exists(os.path.join(Main.wdr, "store", opath)))
 