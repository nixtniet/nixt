# This file is placed in the Public Domain.


"persist tests"


import os
import sys
import unittest


sys.path.insert(0, ".")


from nixt.command import Main
from nixt.objects import Data
from nixt.persist import Disk


Main.wdr = '.test'


class TestPersist(unittest.TestCase):

    def test_save(self):
        obj = Data()
        opath = Disk.write(obj)
        self.assertTrue(os.path.exists(os.path.join(
                                                    Main.wdr,
                                                    "store",
                                                    opath
                                                   )))
