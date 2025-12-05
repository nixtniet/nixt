# This file is placed in the Public Domain.


import unittest


from nixt.objects import Object
from nixt.serials import Json


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = Json.loads(Json.dumps(obj))
        self.assertEqual(oobj["test"], "bla")

    def test_doctest(self):
        self.assertTrue(__doc__ is None)
