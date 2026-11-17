# This file is placed in the Public Domain.


"buffers"


import unittest


from nixt.clients import Buffered


class TestBuffer(unittest.TestCase):

    "buffer unittests"

    def test_construct(self):
        "test biffer construction."
        buffer = Buffered()
        self.assertTrue(type(buffer), Buffered)
