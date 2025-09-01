# This file is placed in the Public Domain.


"parse"


import unittest


from nixt.command import parse
from nixt.objects import Object


class TestParse(unittest.TestCase):

    def test_parse(self):
        obj = Object()
        result = parse(obj, "cmd")
        self.assertEqual(result, None)
