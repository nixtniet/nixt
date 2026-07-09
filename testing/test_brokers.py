# This file is placed in the Public Domain.


"an object for a string"


import unittest


from nixt.defines import Broker, Object


class TestBroker(unittest.TestCase):

    def setUp(self):
        self.broker = Broker()

    def test_add(self):
        obj = Object()
        self.broker.add(obj)
        self.assertTrue(repr(obj) in self.broker.objects)

    def test_get(self):
        pass

    def test_has(self):
        pass

    def test_like(self):
        pass

    def test_objs(self):
        pass
