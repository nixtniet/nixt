# This file is placed in the Public Domain.


import os
import sys
import unittest


sys.path.insert(0, ".")


from bigtalk.persist import Disk, Workdir
from bigtalk.objects import Object


Workdir.wdr = '.test'


class TestPersist(unittest.TestCase):

    def test_save(self):
        obj = Object()
        opath = Disk.write(obj)
        self.assertTrue(os.path.exists(os.path.join(Workdir.wdr, "store", opath)))
