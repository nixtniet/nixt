# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.message import Message
from nixt.objects import Base
from nixt.parsers import Parse


class TestParse(unittest.TestCase):

    def test_parse(self):
        obj = Base()
        Parse.parse(obj, "cmd")        
        self.assertEqual(obj.cmd, "cmd")
