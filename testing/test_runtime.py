# This file is placed in the Public Domain.


"runtime"


import unittest


from nixt.run import Scripts


class TestRuntime(unittest.TestCase):

    def test_scripts(self):
        self.assertTrue(Scripts.background)
