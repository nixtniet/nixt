# This file is placed in the Public Domain.


"utilities"


import unittest


from nixt.runtime import elapsed


class TestUtilities(unittest.TestCase):

    def test_elapsed(self):
        result = elapsed(0)
        self.assertEqual(result, "0.00s")
