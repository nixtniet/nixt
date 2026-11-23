# This file is placed in the Public Domain.


"filem monitor"


import unittest


from nixt.defines import Watcher


class TestObserver(unittest.TestCase):

    "watcher unittests"

    def test_construct(self):
        "test watcher construction."
        watch = Watcher()
        self.assertTrue(type(watch), Watcher)
