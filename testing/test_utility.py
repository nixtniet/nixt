# This file is placed in the Public Domain.


"utilities"


import unittest


from nixt.utility import Utils


class TestUtilities(unittest.TestCase):

    def test_pkgname(self):
        self.assertEqual(Utils.pkgname(Utils), "nixt")
