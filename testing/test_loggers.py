# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.defines import Logging


class TestLoggers(unittest.TestCase):

    def test_dateformat(self):
        self.assertTrue(Logging.datefmt)
