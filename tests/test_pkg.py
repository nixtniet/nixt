# This file is placed in the Public Domain.


"package"


import unittest


from nixt.pkg import Mods


class TestPackage(unittest.TestCase):

    def test_construct(self):
        mods = Mods()
        self.assertEqual(type(mods), Mods)
