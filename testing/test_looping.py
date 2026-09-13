# This file is placed in the Public Domain.


"looping"


import unittest


from nixt.looping import Loop


class TestLoop(unittest.TestCase):

    def test_construct(self):
        loop = Loop()
        self.assertTrue(type(loop), Loop)
