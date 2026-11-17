# This file is placed in the Public Domain.


"runners"


import unittest


from nixt.pooling import Pool


class TestRunner(unittest.TestCase):

    "runner unittests"

    def test_construct(self):
        "test runner construction."
        pool = Pool()
        self.assertTrue(type(pool), Pool)
