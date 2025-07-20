# This file is placed in the Public Domain.


"tests utilities"


import unittest


from nixt.utils import elapsed, spl


class TestComposite(unittest.TestCase):

    def test_spl(self):
        spll = spl("a,b,c")
        self.assertEqual(spll, ["a", "b", "c"])
