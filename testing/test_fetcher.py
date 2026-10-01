# This file is placed in the Public Domain.


"fetcher"


import unittest


from nixt.fetcher import Fetcher


class TestFetcher(unittest.TestCase):

    "fetcher unittests"

    def test_construct(self):
        "test fetcher construction."
        fetcher = Fetcher()
        self.assertTrue(type(fetcher), Fetcher)
