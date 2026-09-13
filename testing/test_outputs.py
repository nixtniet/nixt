# This file is placed in the Public Domain.


"output"


import unittest


from nixt.buffers import Output


class TestOutput(unittest.TestCase):

    def test_construct(self):
        output = Output()
        self.assertTrue(type(output), Output)
