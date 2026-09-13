# This file is placed in the Public Domain.


"time related"


import unittest


from nixt.defines import Time


class TestTime(unittest.TestCase):

    def construct(self):
        time = Time()
        self.assertTrue(type(time), Time)

    def test_times(self):
        self.assertTrue(Time.times)
