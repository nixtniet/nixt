# This file is placed in the Public Domain.


"decoder/encoder"


import unittest


from nixt.object import Object
from nixt.serial import dumps, loads


class TestSerial(unittest.TestCase):

    def test_dumps(self):
        obj = Object()
        result = dumps(obj)
        self.assertEqual(result, '{}')
