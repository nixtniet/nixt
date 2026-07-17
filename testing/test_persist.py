# This file is placed in the Public Domain.


"persist tests"


import sys
import unittest


sys.path.insert(0, ".")


from nixt.persist import Cache, Disk, Workdir


Workdir.wdr = '.test'


class TestCache(unittest.TestCase):

    def test_construct(self):
        cache = Cache()
        self.assertTrue(cache)

    def test_add(self):
        pass

    def test_get(self):
        pass

    def test_sync(self):
        pass


class TestDisk(unittest.TestCase):

    def test_construct(self):
        disk = Disk()
        self.assertTrue(disk)

    def test_ident(self):
        pass

    def test_read(self):
        pass

    def test_write(self):
        pass


class TestWorkdir(unittest.TestCase):

    def test_construct(self):
        wdr = Workdir()
        self.assertTrue(wdr)

    def test_home(self):
        pass

    def test_kinds(self):
        pass

    def test_lomg(self):
        pass

    def test_moddir(self):
        pass

    def test_pid(self):
        pass

    def test_skel(self):
        pass
