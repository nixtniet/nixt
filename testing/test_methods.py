# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.objects import Object, Method


class TestMethod(unittest.TestCase):

    def test_clear(self):
        obj = Object()
        obj.a = "b"
        Method.clear(obj)
        self.assertEqual(str(obj), "{}")

    def test_clz(self):
        pass

    def test_construct(self):
        pass

    def test_copy(self):
        pass

    def test_deleted(self):
        pass

    def test_edit(self):
        pass

    def test_fmt(self):
        pass

    def test_fqn(self):
        pass

    def test_fromkeys(self):
        pass

    def test_get(self):
        pass

    def test_items(self):
        pass

    def test_keys(self):
        pass

    def test_merge(self):
        pass

    def test_notset(self):
        pass

    def test_pop(self):
        pass

    def test_popitem(self):
        pass

    def test_reduce(self):
        pass

    def test_search(self):
        pass

    def test_skip(self):
        pass

    def test_typed(self):
        pass

    def test_update(self):
        pass

    def test_values(self):
        pass

 