# This file is placed in the Public Domain.


"runners"


import unittest


from nixt.runners import Runners


class TestRunners(unittest.TestCase):

    "runner unittests"

    def test_construct(self):
        "test runner construction."
        runners = Runners()
        self.assertTrue(type(runners), Runners)
