# This file is placed in the Public Domain.


"runners"


import unittest


from nixt.runners import Runner


class TestRunner(unittest.TestCase):

    def test_construct(self):
        runner = Runner()
        self.assertTrue(type(runner), Runner)
