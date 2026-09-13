# This file is placed in the Public Domain.


"fetcher"


import unittest


from nixt.fetcher import Fetcher


class TestFetcher(unittest.TestCase):

    def test_construct(self):
        fetcher = Fetcher()
        self.assertTrue(type(fetcher), Fetcher)
