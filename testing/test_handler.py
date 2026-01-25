# This file is placed in the Public Domain.


"engine"


import unittest


from nixt.handler import Client, Handler
from nixt.message import Message


def hello(event):
    event.reply("hello")
    event.ready()


class TestHandler(unittest.TestCase):

    def testcomposite(self):
        eng = Handler()
        self.assertEqual(type(eng), Handler)


class TestHandler(unittest.TestCase):

    clt = Client()

    def setUp(self):
        self.clt.register("hello", hello)
        self.clt.start()

    def shutDown(self):
        self.clt.stop()

    def test_loop(self):
        e = Message()
        e.kind = "hello"
        self.clt.put(e)
        e.wait()
        self.assertTrue(True)
