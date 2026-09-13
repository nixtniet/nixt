# This file is placed in the Public Domain.


"logging"


import unittest


from nixt.loggers import Format, Logging


class TestFormat(unittest.TestCase):

    def test_construct(self):
        fmt = Format()
        self.assertTrue(type(fmt), Format)


class TestLogging(unittest.TestCase):

    def test_construct(self):
        logger = Logging()
        self.assertTrue(type(logger), Logging)
