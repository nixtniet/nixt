# This file is placed in the Public Domain.


"buffers"


import unittest


from nixt.buffers import Buffer


class TestBuffer(unittest.TestCase):

    def test_construct(self):
        buffer = Buffer()
        self.assertTrue(type(buffer), Buffer)
