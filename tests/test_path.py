# This file is placed in the Public Domain.


import unittest
import os
import shutil
import datetime


from nixt.path import Workdir, getpath, ident, long, pidname, skel, store, strip, types, wdr
from nixt.object import Object


TEST_WORKDIR = ".test_workdir"


class TestPath(unittest.TestCase):

    def setUp(self):
        Workdir.wdr = TEST_WORKDIR
        os.makedirs(os.path.join(TEST_WORKDIR, "store"), exist_ok=True)

    def tearDown(self):
        if os.path.exists(TEST_WORKDIR):
            shutil.rmtree(TEST_WORKDIR)

    def test_ident(self):
        pass

    def test_long(self):
        pass

    def test_pidname(self):
        pass

    def test_skel(self):
        pass

    def test_store(self):
        pass

    def test_strip(self):
        pass

    def test_types(self):
        pass

    def test_wdr(self):
        pass


if __name__ == '__main__':
    unittest.main()
