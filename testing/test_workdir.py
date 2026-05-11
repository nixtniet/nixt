# This file is placed in the Public Domain.


"working directory"


import unittest


from nixt.persist import Workdir


class TestWorkdir(unittest.TestCase):

    def test_construct(self):
        self.assertEqual(Workdir.wdr, ".test")
