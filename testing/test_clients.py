# This file is placed in the Public Domain.


"engine"


import unittest


from nixt.defines import Message, Screen


buffer = []


def hello(message):
    message.reply(message.text)
    message.ready()


class MyClient(Screen):

    def __init__(self):
        Screen.__init__(self)
        self.register("hello", hello)

    def raw(self, text):
        buffer.append(text)


class TestClient(unittest.TestCase):

    def setUp(self):
        self.clt = MyClient()
        self.clt.silent = False
        self.clt.start()

    def shutDown(self):
        self.clt.stop()

    def test_announce(self):
        self.clt.announce("hello")
        self.assertTrue("hello" in buffer)

    def test_display(self):
        msg = Message()
        msg.reply("test1")
        msg.reply("test2")
        self.clt.display(msg)
        self.assertTrue("test1" in buffer)
        self.assertTrue("test2" in buffer)
        self.assertTrue(buffer.index("test1") < buffer.index("test2"))

    def test_dosay(self):
        self.clt.dosay("#channel", "yo!")
        self.assertTrue("yo!" in buffer)

    def test_put(self):
        msg = Message()
        msg.kind = "hello"
        msg.text = "hi world"
        self.clt.put(msg)
        msg.wait()
        self.assertTrue("hi world" in msg.result)
