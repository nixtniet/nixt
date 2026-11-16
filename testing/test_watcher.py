# This file is placed in the Public Domain.


"filem monitor"


import unittest


from nixt.defines import Watcher


class TestWatcher(unittest.TestCase):

    "watcher unittests"

    def test_construct(self):
        "test watcher construction."
        watcher = Watcher()
        self.assertTrue(type(watcher), Watcher)
