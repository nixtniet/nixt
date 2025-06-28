# This file is placed in the Public Domain.


import unittest
import os
import shutil
import time


from nixt.disk   import Error, cdir, read, write
from nixt.find   import find, fns, last, search
from nixt.object import Object, fqn
from nixt.path   import store, long


TEST_STORE = ".test_store"


class TestDisk(unittest.TestCase):

    def setUp(self):
        os.makedirs(TEST_STORE, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(TEST_STORE)

    def test_cdir(self):
        pass

    def test_write_and_read(self):
        pass

    def test_read_error(self):
        pass

    def test_fns_and_find(self):
        pass

    def test_last(self):
        pass

    def test_search(self):
        pass


if __name__ == "__main__":
    unittest.main()
