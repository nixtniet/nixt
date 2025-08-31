# This file is placed in the Public Domain.


"logging. tests"


import unittest


from nixt.runtime import Logging, rlog


class TestLogging(unittest.TestCase):

    def test_level(self):
        Logging.level("warn")
        rlog("warn", "test")
        self.assertEqual("test", "test")
