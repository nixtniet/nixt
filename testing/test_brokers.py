# This file is placed in the Public Domain.


import unittest


from nixt.brokers import Broker
from nixt.handler import Client
from nixt.serials import dumps, loads


from nixbot.objects import Object, update, values


class TestBroker(unittest.TestCase):

    def test_update(self):
        o = {}
        o["a"] = "b"
        update(Broker, o)
        self.assertEqual(Broker.a, "b")

    def test_json(self):
        Broker.a = "b"
        s = dumps(Broker)
        o = loads(s)
        self.assertEqual(o["a"], "b")

    def test_add(self):
        clt = Client()
        self.assertTrue(clt in values(Broker.objects))
