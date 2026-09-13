# This file is placed in the Public Domain.


"watcher"


import unittest


from nixt.watcher import Watcher


class TestWatcher(unittest.TestCase):

    def test_construct(self):
        watcher = Watcher()
        self.assertTrue(type(watcher), Watcher)
