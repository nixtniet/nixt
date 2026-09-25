# This file is placed in the Public Domain.


"an object for a string"


import unittest


from nixt.defines import Broker, Object


class TestBroker(unittest.TestCase):

    broker = Broker()

    def test_construct(self):
        broker = Broker()
        self.assertTrue(broker.objects)

    def test_add(self):
        obj = Object()
        self.broker.add(obj)
        self.assertTrue(obj in self.broker.objects.values())

    def test_get(self):
        obj = Object()
        self.broker.add(obj)
        obj2 = self.broker.get(repr(obj))
        self.assertEqual(obj, obj2)

    def test_has(self):
        obj = Object()
        self.broker.add(obj)
        self.assertTrue(self.broker.has(obj))

    def test_like(self):
        obj = Object()
        self.broker.add(obj)
        self.assertTrue(repr(obj) in [x[0] for x in self.broker.like("object")])

    def test_remove(self):
        obj = Object()
        self.broker.add(obj)
        self.broker.remove(obj)
        self.assertTrue(obj not in self.broker.objects.values())
