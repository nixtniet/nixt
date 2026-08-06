# This file is placed in the Public Domain.


"time related"


import unittest


from nixt import Time


class TestTime(unittest.TestCase):

    def test_times(self):
        self.assertTrue(Time.times)
