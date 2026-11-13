# This file is placed in the Public Domain.


"filem monitor"


import unittest


from nixt.defines import Monitor


class TestWatcher(unittest.TestCase):

    "watcher unittests"

    def test_construct(self):
        "test watcher construction."
        watcher = Monitor()
        self.assertTrue(type(watcher), Monitor)
