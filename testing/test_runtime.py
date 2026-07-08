# This file is placed in the Public Domain.


"runtime tests"


import unittest


from nixt.runtime import CLI, main


class TestRuntime(unittest.TestCase):

    def test_construct(self):
        cli = CLI()
        self.assertTrue(cli)

    def test_main(self):
        pass
