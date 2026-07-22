# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.loggers import Logging


class TestLogging(unittest.TestCase):

    def test_construct(self):
        logger = Logging()
        self.assertTrue(logger)

    def test_level(self):
        pass

    def test_size(self):
        pass
