# This file is placed in the Public Domain.


import unittest


from nixt.brokers import broker
from nixt.handler import Client
from nixt.encoder import dumps, loads
from nixt.objects import Object, update


result = []


def announce(txt):
    result.append(txt)


class TestBroker(unittest.TestCase):

    def test_add(self):
        obj = Object()
        broker.add(obj)
        self.assertTrue(broker.has(obj))

    def test_announce(self):
        clt = Client()
        clt.announce = announce
        broker.announce("test")
        self.assertTrue("test" in result)

    def test_get(self):
        obj = Object()
        broker.add(obj)
        oobj = broker.get(repr(obj))
        self.assertTrue(oobj is obj)

    def test_objs(self):
        clt = Client()
        objs = broker.objs("announce")
        self.assertTrue(clt in objs)

    def test_has(self):
        obj = Object()
        broker.add(obj)
        self.assertTrue(broker.has(obj))

    def test_like(self):
        obj = Object()
        broker.add(obj)
        self.assertTrue(broker.like(repr(obj)))

    def test_json(self):
        broker.a = "b"
        s = dumps(broker)
        o = loads(s)
        self.assertEqual(o["a"], "b")
        
    def test_update(self):
        o = {}
        o["a"] = "b"
        update(broker, o)
        self.assertEqual(broker.a, "b")
