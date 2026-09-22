# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.defines import Object, Parser


class TestParse(unittest.TestCase):

    def test_parse(self):
        obj = Object()
        obj.cmd = ""
        Parser.parse(obj, "cmd")
        self.assertEqual(obj.cmd, "cmd")
