# This file is placed in the Public Domain.


"module management"


import unittest


from nixt.defines import Mods


class TestMods(unittest.TestCase):

    def test_construct(self):
        mods = Mods()
        self.assertTrue(type(mods), Mods)

    def test_dir(self):
        Mods.dir("mods", "mods")
        self.assertTrue("mods" in Mods.dirs)
