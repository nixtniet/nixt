# This file is placed in the Public Domain.


"package"


import unittest


from nixt.package import Mods


class TestPackage(unittest.TestCase):

    def test_init(self):
        Mods.init("mod", "mod")
        self.assertTrue("mod" in Mods.dirs)
