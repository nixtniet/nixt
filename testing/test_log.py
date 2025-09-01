# This file is placed in the Public Domain.


"logging. tests"


import unittest


from nixt.runtime import level, rlog


class TestLogging(unittest.TestCase):

    def test_level(self):
        level("warn")
        rlog("warn", "test")
        self.assertEqual("test", "test")
