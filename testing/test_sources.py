# This file is placed in the Public Domain.


"md5sums"


import unittest


from nixt.sources import MD5


class TestMD5(unittest.TestCase):

    def test_construct(self):
        md5 = MD5()
        self.assertTrue(type(md5), MD5)
