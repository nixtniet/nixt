# This file is placed in the Public Domain.


"require"


import unittest


from nixt.require import Cmd


class TestCmd(unittest.TestCase):

    def test_construct(self):
        cmd = Cmd()
        self.assertTrue(type(cmd), Cmd)
