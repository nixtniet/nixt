# This file is placed in the Public Domain.


"methods"


import unittest


from nixt.methods import *
from nixt.objects import Object


class TestMethods(unittest.TestCase):

    def test_deleted(self):
        obj = Object()
        obj.__deleted__ = True
        self.assertTrue(deleted(obj))

    def test_edit(self):
        obj = Object()
        dct = {"a": "b"}
        edit(obj, dct)
        self.assertEqual(obj.a, "b")

    def test_fmt(self):
        obj = Object()
        obj.a = "b"
        self.assertTrue(fmt(obj), 'a="b"')

    def test_fqn(self):
        obj = Object()
        self.assertTrue(fqn(obj), "nixt.objects.Object")

    def test_ident(self):
        obj = Object()
        self.assertTrue("nixt.objects.Object" in ident(obj))

    def test_merge(self):
        obj = Object()
        obj.a = "b"
        merge(obj, {"a": ""})
        self.assertEqual(obj.a, "b")

    def test_parse(self):
        obj = Object()
        parse(obj, "cmd")
        self.assertEqual(obj.cmd, "cmd")

    def test_reduce(self):
        obj = Object()
        obj.a = "b"
        obj.b = ""
        dct = reduce(obj)
        self.assertTrue("b" not in dct)

    def test_search(self):
        obj = Object()
        obj.a = "b"
        self.assertTrue(search(obj, {"a": "b"}))

    def test_skip(self):
        obj = Object()
        obj.a = "b"
        obj.b = "c"
        dct = skip(obj, "b")
        self.assertTrue("b" not in dct)

    def test_typed(self):
        obj = Object()
        typed(obj, "a", "true")
        self.assertTrue(obj.a)
