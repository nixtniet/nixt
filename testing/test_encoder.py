# This file is placed in the Public Domain.


"encoder/decoder tests"


import unittest


from nixt.encoder import Json
from nixt.objects import Object, Data


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_dumps(self):
        obj = Data()
        obj.test = "bla"
        self.assertEqual(Json.dumps(obj), VALIDJSON)


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Data()
        obj.test = "bla"
        oobj = Json.loads(Json.dumps(obj))
        self.assertEqual(oobj["test"], "bla")


class TestTypes(unittest.TestCase):

    def test_dict(self):
        obj = Json.loads(Json.dumps({"a": "b"}))
        self.assertEqual(obj, {"a": "b"})

    def test_integer(self):
        obj = Json.loads(Json.dumps(1))
        self.assertEqual(obj, 1)

    def test_float(self):
        obj = Json.loads(Json.dumps(1.0))
        self.assertEqual(obj, 1.0)

    def test_string(self):
        obj = Json.loads(Json.dumps("test"))
        self.assertEqual(obj, "test")

    def test_true(self):
        obj = Json.loads(Json.dumps(True))
        self.assertEqual(obj, True)

    def test_false(self):
        obj = Json.loads(Json.dumps(False))
        self.assertEqual(obj, False)

    def test_object(self):
        ooo = Data()
        ooo.a = "b"
        obj = Data()
        Object.update(obj, Json.loads(Json.dumps(ooo)))
        self.assertEqual(obj.a, "b")
