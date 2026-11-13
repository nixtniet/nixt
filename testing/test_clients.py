# This file is placed in the Public Domain.
# pylint: disable=C0103


"client tests"


import unittest


from nixt.defines import Client, Message


buffer = []


def hello(message):
    "command."
    message.reply(message.text)
    message.ready()


class MyClient(Client):

    "clients raw puts text into buffer"

    def __init__(self):
        Client.__init__(self)
        self.register("hello", hello)

    def raw(self, text):
        "add text to buffer."
        buffer.append(text)


class TestClient(unittest.TestCase):

    "clients unittest."

    def setUp(self):
        self.clt = MyClient()
        self.clt.silent = False
        self.clt.start()

    def shutDown(self):
        "shutdown client"
        self.clt.stop()

    def test_announce(self):
        "test announce."
        self.clt.announce("hello")
        self.assertTrue("hello" in buffer)

    def test_construct(self):
        "test client construction."
        client = MyClient()
        self.assertTrue(type(client), MyClient)

    def test_display(self):
        "test display function."
        msg = Message()
        msg.reply("test1")
        msg.reply("test2")
        self.clt.display(msg)
        self.assertTrue("test1" in buffer)
        self.assertTrue("test2" in buffer)
        self.assertTrue(buffer.index("test1") < buffer.index("test2"))

    def test_dosay(self):
        "test called from external say (dosay)."
        self.clt.dosay("#channel", "yo!")
        self.assertTrue("yo!" in buffer)

    def test_put(self):
        "test putting event to the client."
        msg = Message()
        msg.kind = "hello"
        msg.text = "hi world"
        self.clt.put(msg)
        msg.wait()
        self.assertTrue("hi world" in msg.result)
