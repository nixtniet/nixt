# This file is placed in the Public Domain.


"obejcts tests"


import unittest


from nixt.objects import Data, Object, Methods


import nixt.objects


TARGET = nixt.objects
VALIDJSON = '{"test": "bla"}'


class TestObject(unittest.TestCase):

    def test_constructor(self):
        obj = Data()
        self.assertTrue(type(obj), Data)

    def test_class(self):
        obj = Data()
        clz = obj.__class__()
        self.assertTrue("Data" in str(type(clz)))

    def test_contains(self):
        obj = Data()
        obj.key = "value"
        self.assertTrue("key" in obj)

    def test_delattr(self):
        obj = Data()
        obj.key = "value"
        del obj.key
        self.assertTrue("key" not in obj)

    def test_dict(self):
        obj = Data()
        self.assertEqual(obj.__dict__, {})

    def test_doc(self):
        obj = Data()
        self.assertEqual(obj.__doc__, None)

    def test_format(self):
        obj = Data()
        self.assertEqual(format(obj, ""), "{}")

    def test_getattribute(self):
        obj = Data()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key", None), "value")

    def test_hash__(self):
        obj = Data()
        hsj = hash(obj)
        self.assertTrue(isinstance(hsj, int))

    def test_init(self):
        obj = Data()
        self.assertTrue(type(Data.__init__(obj)), Data)

    def test_iter(self):
        obj = Data()
        obj.key = "value"
        self.assertTrue(list(iter(obj)), ["key",])

    def test_getattr(self):
        obj = Data()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key"), "value")

    def test_keys(self):
        obj = Data()
        obj.key = "value"
        self.assertEqual(list(Object.keys(obj)), ["key"])

    def test_len(self):
        obj = Data()
        self.assertEqual(len(obj), 0)

    def test_items(self):
        obj = Data()
        obj.key = "value"
        self.assertEqual(list(Object.items(obj)), [("key", "value")])

    def test_register(self):
        obj = Data()
        setattr(obj, "key", "value")
        self.assertEqual(obj.key, "value")

    def test_repr(self):
        self.assertTrue(
                        repr(Object.update(Data(), {"key": "value"})),
                        {"key": "value"}
                       )

    def test_setattr(self):
        obj = Data()
        setattr(obj, "key", "value")
        self.assertTrue(obj.key, "value")

    def test_str(self):
        obj = Data()
        self.assertEqual(str(obj), "{}")

    def test_update(self):
        obj = Data()
        obj.key = "value"
        oobj = Data()
        Object.update(oobj, obj)
        self.assertTrue(oobj.key, "value")

    def test_values(self):
        obj = Data()
        obj.key = "value"
        self.assertEqual(list(Object.values(obj)), ["value"])


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Data()
        obj.obj = Data()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")


class TestMethods(unittest.TestCase):

    def testformat(self):
        o = Data()
        o.a = "b"
        self.assertEqual(Methods.fmt(o), 'a="b"')
