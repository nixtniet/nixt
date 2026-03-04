# This file is placed in the Public Domain.


"package"


import unittest


from bigtalk.package import Mods


class TestPackage(unittest.TestCase):

    def test_add(self):
        Mods.add("mods", "mods")
        self.assertTrue("mods" in Mods.dirs)
