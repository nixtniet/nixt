# This file is placed in the Public Domain.


"persist tests"


import os
import unittest


from nixt.defines import Disk, Main, Locater, Method, Workdir
from nixt.persist import Cache


Workdir.wdr = '.test'


class TestCache(unittest.TestCase):

    def test_construct(self):
        cache = Cache()
        self.assertTrue(type(cache), Cache)


class TestDisk(unittest.TestCase):

    def test_construct(self):
        disk = Disk()
        self.assertTrue(type(disk), Disk)

    def test_loadcfg(self):
        Main.a = "b"
        Disk.read(Main, "main", "config")
        self.assertEqual(Main.a, "b")

    def test_save(self):
        obj = Method()
        opath = Disk.write(obj)
        self.assertTrue(os.path.exists(os.path.join(Workdir.wdr, "store", opath)))

    def test_writecfg(self):
        Main.a = "b"
        Disk.write(Main, "main", "config")
        self.assertTrue(os.path.exists(os.path.join(Workdir.wdr, "config", "main")))


class TestLocater(unittest.TestCase):

    def test_construct(self):
        locater = Locater()
        self.assertTrue(type(locater), Locater)


class TestWorkdir(unittest.TestCase):

    def test_construct(self):
        workdir = Workdir()
        self.assertTrue(type(workdir), Workdir)
