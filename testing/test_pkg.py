# This file is placed in the Public Domain.


"package"


import unittest


from nixt.modules import Mods


class TestPackage(unittest.TestCase):

    def test_construct(self):
        mds = Mods()
        self.assertEqual(type(mds), Mods)
