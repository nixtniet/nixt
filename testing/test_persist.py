# This file is placed in the Public Domain.


import os
import sys
import unittest


sys.path.insert(0, ".")


from nixt.objects import Object
from nixt.persist import Cache, Workdir, write


import nixt.persist


TARGET = nixt.persist


Workdir.wdr = '.test'


ATTRS1 = (
    'Cache',
    'Workdir',
    'addpath',
    'find',
    'getpath',
    'kinds',
    'last',
    'pidfile',
    'pidname',
    'read',
    'setwd',
    'skel',
    'strip',
    'syncpath',
    'workdir',
    'write'
)


class TestPersist(unittest.TestCase):

    def test_interface(self):
        self.assertEqual(dir(TARGET),list(ATTRS1))

    def test_save(self):
        obj = Object()
        opath = write(obj)
        self.assertTrue(os.path.exists(os.path.join(Workdir.wdr, "store", opath)))
