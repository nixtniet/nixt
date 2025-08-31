# This file is placed in the Public Domain.


"utilities"


import unittest


from nixt.runtime import Time


class TestUtilities(unittest.TestCase):

    def test_elapsed(self):
        result = Time.elapsed(0)
        self.assertEqual(result, "0.00s")
