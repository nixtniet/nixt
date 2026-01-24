# This file is placed in the Public Domain.


import os
import sys
import unittest


sys.path.insert(0, ".")


from nixt.objects import Object
from nixt.persist import Cache, write


import nixt.persist


TARGET = nixt.persist


Cache.workdir = '.test'


ATTRS1 = (
    'Cache',
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



class TestStorage(unittest.TestCase):

    def test_constructor(self):
        obj = Cache()
        self.assertTrue(type(obj), Cache)

    def test__class(self):
        obj = Cache()
        clz = obj.__class__()
        self.assertTrue('Cache' in str(type(clz)))

    def test_dirmodule(self):
        self.assertEqual(
                         dir(TARGET),
                         list(ATTRS1)
                        )

    def test_module(self):
        self.assertTrue(Cache().__module__, 'Cache')

    def test_save(self):
        obj = Object()
        opath = write(obj)
        print(opath)
        self.assertTrue(os.path.exists(os.path.join(Cache.workdir, "store", opath)))
