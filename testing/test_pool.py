# This file is placed in the Public Domain.


"runners"


import unittest


from nixt.defines import Pool


class TestPool(unittest.TestCase):

    "runner unittests"

    def test_construct(self):
        "test runner construction."
        pool = Pool()
        self.assertTrue(type(pool), Pool)
