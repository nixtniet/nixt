# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.defines import Object, Parse


class TestParse(unittest.TestCase):

    def test_parse(self):
        obj = Object()
        obj.cmd = ""
        Parse.parse(obj, "cmd")
        print(obj)
        self.assertEqual(obj.cmd, "cmd")
