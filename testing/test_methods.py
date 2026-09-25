# This file is placed in the Public Domain.
# type: ignore
# pylint: disable=W0201


"logging tests"


import unittest


from nixt.defines import Object, Method


class Mine(Object):

    pass


class TestMethod(unittest.TestCase):

    def test_construct(self):
        method = Method()
        self.assertTrue(type(method), Method)

    def test_clear(self):
        obj = Mine()
        obj.a = "b"
        Method.clear(obj)
        self.assertEqual(str(obj), "{}")

    def test_class(self):
        obj = Mine()
        clz = obj.__class__()
        self.assertTrue("Mine" in str(type(clz)))

    def test_contains(self):
        obj = Mine()
        obj.key = "value"
        self.assertTrue("key" in obj)

    def test_delattr(self):
        obj = Mine()
        obj.key = "value"
        del obj.key
        self.assertTrue("key" not in obj)

    def test_dict(self):
        obj = Mine()
        self.assertEqual(obj.__dict__, {})

    def test_format(self):
        obj = Mine()
        self.assertEqual(format(obj, ""), "{}")

    def test_getattribute(self):
        obj = Mine()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key", None), "value")

    def test_hash__(self):
        obj = Mine()
        hsj = hash(obj)
        self.assertTrue(isinstance(hsj, int))

    def test_init(self):
        obj = Mine()
        Object.__init__(obj)
        self.assertTrue(type(obj), Mine)

    def test_iter(self):
        obj = Mine()
        obj.key = "value"
        self.assertTrue(list(iter(obj)), ["key",])

    def test_format2(self):
        o = Mine()
        o.a = "b"
        self.assertEqual(Method.fmt(o), 'a="b"')

    def test_getattr(self):
        obj = Mine()
        obj.key = "value"
        self.assertEqual(obj.key, "value")

    def test_keys(self):
        obj = Mine()
        obj.key = "value"
        self.assertEqual(list(Method.keys(obj)), ["key"])

    def test_len(self):
        obj = Mine()
        self.assertEqual(len(obj), 0)

    def test_items(self):
        obj = Mine()
        obj.key = "value"
        self.assertEqual(list(Method.items(obj)), [("key", "value")])

    def test_repr(self):
        self.assertTrue(
                        repr(Method.update(Object(), {"key": "value"})),
                        {"key": "value"}
                       )

    def test_setattr(self):
        obj = Mine()
        obj.key = "value"
        self.assertTrue(obj.key, "value")

    def test_str(self):
        obj = Mine()
        self.assertEqual(str(obj), "{}")

    def test_update(self):
        obj = Mine()
        obj.key = "value"
        oobj = Mine()
        Method.update(oobj, obj)
        self.assertTrue(oobj.key, "value")

    def test_values(self):
        obj = Mine()
        obj.key = "value"
        self.assertEqual(list(Method.values(obj)), ["value"])
