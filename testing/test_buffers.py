# This file is placed in the Public Domain.


"buffers"


import unittest


from nixt.clients import BufferedClient


class TestBuffer(unittest.TestCase):

    "buffer unittests"

    def test_construct(self):
        "test biffer construction."
        buffer = BufferedClient()
        self.assertTrue(type(buffer), BufferedClient)
