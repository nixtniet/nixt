# This file is placed in the Public Domain.


import os
import unittest


from nixt.encoder import dump, dumps, load, loads
from nixt.objects import Object, update
from nixt.persist import workdir


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_dump(self):
        obj = Object()
        obj.test = "bla"
        path = workdir("test")
        with open(path, "w", encoding="utf-8") as file:
            dump(obj, file)
        self.assertTrue(os.path.exists(path))
        oobj = Object()
        with open(path, "r", encoding="utf-8") as file:
            oobj = load(file)
        self.assertTrue(oobj["test"] == "bla")

    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)


class TestDecoder(unittest.TestCase):

    def test_load(self):
        obj = Object()
        obj.test = "bla"
        path = workdir("test2")
        with open(path, "w", encoding="utf-8") as file:
            dump(obj, file)
        self.assertTrue(os.path.exists(path))
        oobj = Object()
        with open(path, "r", encoding="utf-8") as file:
           oobj = load(file)
        self.assertTrue(oobj["test"] == "bla")

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj["test"], "bla")


class TestTypes(unittest.TestCase):

    def test_dict(self):
        obj = loads(dumps({"a": "b"}))
        self.assertEqual(obj, {"a": "b"})

    def test_integer(self):
        obj = loads(dumps(1))
        self.assertEqual(obj, 1)

    def test_float(self):
        obj = loads(dumps(1.0))
        self.assertEqual(obj, 1.0)

    def test_string(self):
        obj = loads(dumps("test"))
        self.assertEqual(obj, "test")

    def test_true(self):
        obj = loads(dumps(True))
        self.assertEqual(obj, True)

    def test_false(self):
        obj = loads(dumps(False))
        self.assertEqual(obj, False)

    def test_object(self):
        ooo = Object()
        ooo.a = "b"
        obj = Object()
        update(obj, loads(dumps(ooo)))
        self.assertEqual(obj.a, "b")
