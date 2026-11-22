# This file is placed in the Public Domain.


"filem monitor"


import unittest


from nixt.defines import Observer


class TestObserver(unittest.TestCase):

    "watcher unittests"

    def test_construct(self):
        "test watcher construction."
        observer = Observer()
        self.assertTrue(type(observer), Observer)
