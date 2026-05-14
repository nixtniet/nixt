# This file is placed in the Public Domain.


"definitions"


import unittest


import nixt.face as dev


class TestDefines(unittest.TestCase):

    def test_dir(self):
        self.assertTrue(len(dir(dev)), 22)
