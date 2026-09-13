# This file is placed in the Public Domain.


"repeater"


import unittest


from nixt.repeats import Repeater


class TestRepeater(unittest.TestCase):

    def test_construct(self):
        repeater = Repeater()
        self.assertTrue(type(repeater), Repeater)
