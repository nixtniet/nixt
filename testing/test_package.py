# This file is placed in the Public Domain.


"package"


import unittest


from nixt.package import mods


class TestPackage(unittest.TestCase):

    def test_add(self):
        mods.add("mods", "mods")
        self.assertTrue("mods" in mods.dirs)
