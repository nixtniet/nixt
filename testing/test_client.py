# This file is placed in the Public Domain.


"clients"


import unittest


from nixt.handler import Client
from nixt.message import Message


def hello(event):
    event.reply("hello")
    event.ready()


clt = Client()
clt.register("hello", hello)
clt.start()


class TestHandler(unittest.TestCase):

    def test_loop(self):
        e = Message()
        e.type = "hello"
        clt.put(e)
        e.wait()
        self.assertTrue(True)
