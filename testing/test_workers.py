# This file is placed in the Public Domain.


"runners"


import unittest


from nixt.workers import Workers


class TestWorkers(unittest.TestCase):

    "runner unittests"

    def test_construct(self):
        "test runner construction."
        workers = Workers()
        self.assertTrue(type(workers), Workers)
