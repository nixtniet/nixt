# This file is placed in the Public Domain.


"persist tests"


import os
import sys
import unittest


sys.path.insert(0, ".")


from nixt.persist import Disk, Workdir
from nixt.objects import Data


Workdir.wdr = '.test'


class TestPersist(unittest.TestCase):

    def test_save(self):
        obj = Data()
        opath = Disk.write(obj)
        self.assertTrue(os.path.exists(os.path.join(Workdir.wdr, "store", opath)))
