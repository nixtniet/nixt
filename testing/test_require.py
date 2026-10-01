# This file is placed in the Public Domain.


"require"


import unittest


from nixt.require import Cmd


class TestCmd(unittest.TestCase):

    "basic commands unittest"

    def test_construct(self):
        "test command construction."
        cmd = Cmd()
        self.assertTrue(type(cmd), Cmd)
