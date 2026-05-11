# This file is placed in the Public Domain.


"time related"


import unittest


from nixt.utility import TIMES


class TestTime(unittest.TestCase):

    def test_times(self):
        self.assertTrue(TIMES)
