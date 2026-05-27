# This file is placed in the Public Domain.


"logging tests"


import unittest


from bot.defines import Log


class TestLoggers(unittest.TestCase):

    def test_dateformat(self):
        self.assertTrue(Log.datefmt)
