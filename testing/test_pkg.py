# This file is placed in the Public Domain.


"package"


import unittest


from nixt.kernels import Kernel


class TestPackage(unittest.TestCase):

    def test_construct(self):
        krn = Kernel()
        self.assertEqual(type(krn), Kernel)
