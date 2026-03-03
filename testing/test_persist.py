# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0801


"persist tests"


import os
import shutil
import unittest


from nixt.methods import fqn
from nixt.objects import Object
from nixt.runtime import db


db.setwd('.test')


class TestCache(unittest.TestCase):

    def test_add(self):
        obj = Object()
        db.cache.add("test", obj)
        self.assertTrue("test" in db.cache.paths)

    def test_get(self):
        obj = Object()
        db.cache.add("test", obj)
        oobj = db.cache.get("test")
        self.assertTrue(obj is oobj)

    def test_sync(self):
        obj = Object()
        db.cache.add("test", obj)
        db.cache.sync("test", {"a": "b"})
        self.assertEqual(getattr(db.cache.get("test"), "a"), "b")


class TestLocate(unittest.TestCase):

    def test_attrs(self):
        obj = Object()
        obj.a = "b"
        db.write(obj)
        self.assertTrue("a" in db.attrs(fqn(obj)))

    def test_count(self):
        obj = Object()
        obj.a = "b"
        shutil.rmtree(".test")
        db.write(obj)
        self.assertTrue(db.count(fqn(Object)) == 1)

    def test_find(self):
        obj = Object()
        obj.a = "b"
        result = list(db.find(fqn(obj), {"a": "b"}))
        self.assertTrue(len(result) == 1)

    def fns(self):
        obj = Object()
        filenames = db.fns(fqn(obj))
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
        opath = db.write(obj)
        self.assertTrue(os.path.exists(os.path.join(db.wdr, "store", opath)))

    def test_nop(self):
        pass
