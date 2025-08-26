# This file is placed in the Public Domain.


"paths"


import unittest


from nixt.paths import Workdir


class TestPaths(unittest.TestCase):

    def test_construct(self):
        wdr = Workdir()
        self.assertEqual(type(wdr), Workdir)
