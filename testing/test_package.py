# This file is placed in the Public Domain.


"package"


import unittest


from nixt.package import mods


class TestPackage(unittest.TestCase):

    def test_add(self):
        mods.add("mods", "mods")
        self.assertTrue("mods" in mods.dirs)
        del mods.dirs["mods"]

    def test_get(self):
        mods.add("test", "testing")
        mod = mods.get("dbg")
        self.assertTrue("test.dbg" in mods.modules)

    def test_has(self):
        mods.add("test", "testing")
        mod = mods.get("dbg")
        self.assertTrue(mods.has("dbg"))

    def test_importer(self):
        mods.add("test", "testing")
        mod = mods.importer("dbg", "testing/dbg.py")
        self.assertTrue("dbg" in str(mod))

    def test_iter(self):
        mods.add("test", "testing")
        lst = list(mods.iter("dbg"))
        self.assertTrue("dbg" in lst[0])

    def test_list(self):
        mods.add("test", "testing")
        self.assertTrue("dbg" in mods.list())

    def test_pkg(self):
        import testing
        mods.pkg(testing)
        self.assertTrue("testing" in mods.dirs)
