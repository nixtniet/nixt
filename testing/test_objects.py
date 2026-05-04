# This file is placed in the Public Domain.


"obejcts tests"


import unittest


from nixt.defines import Object, Disk, Json, Method, Method


import nixt.objects


TARGET = nixt.objects
VALIDJSON = '{"test": "bla"}'


class TestMethod(unittest.TestCase):

    def test_constructor(self):
        obj = Object()
        self.assertTrue(type(obj), Object)

    def test_class(self):
        obj = Object()
        clz = obj.__class__()
        self.assertTrue("Object" in str(type(clz)))

    def test_contains(self):
        obj = Object()
        obj.key = "value"
        self.assertTrue("key" in obj)

    def test_delattr(self):
        obj = Object()
        obj.key = "value"
        del obj.key
        self.assertTrue("key" not in obj)

    def test_dict(self):
        obj = Object()
        self.assertEqual(obj.__dict__, {})

    def test_doc(self):
        obj = Object()
        self.assertEqual(obj.__doc__, None)

    def test_format(self):
        obj = Object()
        self.assertEqual(format(obj, ""), "{}")

    def test_getattribute(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key", None), "value")

    def test_hash__(self):
        obj = Object()
        hsj = hash(obj)
        self.assertTrue(isinstance(hsj, int))

    def test_init(self):
        obj = Object()
        self.assertTrue(type(Object.__init__(obj)), Object)

    def test_iter(self):
        obj = Object()
        obj.key = "value"
        self.assertTrue(list(iter(obj)), ["key",])

    def test_getattr(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key"), "value")

    def test_keys(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(list(Method.keys(obj)), ["key"])

    def test_len(self):
        obj = Object()
        self.assertEqual(len(obj), 0)

    def test_items(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(list(Method.items(obj)), [("key", "value")])

    def test_read(self):
        obj = Object()
        Disk.read(obj, "bla")
        res = {}
        Method.update(res, obj)
        self.assertEqual(res, {})

    def test_register(self):
        obj = Object()
        setattr(obj, "key", "value")
        self.assertEqual(obj.key, "value")

    def test_repr(self):
        self.assertTrue(
                        repr(Method.update(Object(), {"key": "value"})),
                        {"key": "value"}
                       )

    def test_setattr(self):
        obj = Object()
        setattr(obj, "key", "value")
        self.assertTrue(obj.key, "value")

    def test_str(self):
        obj = Object()
        self.assertEqual(str(obj), "{}")

    def test_update(self):
        obj = Object()
        obj.key = "value"
        oobj = Object()
        Method.update(oobj, obj)
        self.assertTrue(oobj.key, "value")

    def test_values(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(list(Method.values(obj)), ["value"])


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")


class TestMethod(unittest.TestCase):

    def testformat(self):
        o = Object()
        o.a = "b"
        self.assertEqual(Method.fmt(o), 'a="b"')


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(Json.dumps(obj), VALIDJSON)


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
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
        ooo = Object()
        ooo.a = "b"
        obj = Object()
        Method.update(obj, Json.loads(Json.dumps(ooo)))
        self.assertEqual(obj.a, "b")
