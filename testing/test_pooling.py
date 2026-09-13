# This file is placed in the Public Domain.


"pool"


import unittest


from nixt.pooling import Pool


class TestPool(unittest.TestCase):

    def test_construct(self):
        pool = Pool()
        self.assertTrue(type(pool), Pool)
