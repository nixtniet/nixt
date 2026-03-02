# This file is placed in the Public Domain.


"package"


import unittest


from nixt.package import Mods


mods = Mods()


class TestPackage(unittest.TestCase):

    def test_dir(self):
        mods.dir("mods", "mods")
        self.assertTrue("mods" in mods.dirs)
        del mods.dirs["mods"]

    def test_get(self):
        mods.dir("test", "testing")
        mods.get("dbg")
        self.assertTrue("test.dbg" in mods.modules)

    def test_has(self):
        mods.dir("test", "testing")
        self.assertTrue(mods.has("dbg"))

    def test_importer(self):
        mods.dir("test", "testing")
        mod = mods.importer("dbg", "testing/dbg.py")
        self.assertTrue("dbg" in str(mod))

    def test_iter(self):
        mods.dir("test", "testing")
        lst = list(mods.iter("dbg"))
        self.assertTrue("dbg" in lst[0])

    def test_list(self):
        mods.dir("test", "testing")
        self.assertTrue("dbg" in mods.list())

    def test_pkg(self):
        import testing
        mods.pkg(testing)
        self.assertTrue("testing" in mods.dirs)
