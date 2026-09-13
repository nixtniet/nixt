# This file is placed in the Public Domain.


"logging"


import unittest


from nixt.loggers import Logging


class TestLogging(unittest.TestCase):

    def test_construct(self):
        logger = Logging()
        self.assertTrue(type(logger), Logging)
