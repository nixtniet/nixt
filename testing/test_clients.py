# This file is placed in the Public Domain.


"engine"


import unittest


from nixt.defines import Client, Message


buffer = []


def hello(event):
    event.reply(event.text)
    event.ready()


class MyClient(Client):

    def raw(self, text):
        buffer.append(text)


class TestClient(unittest.TestCase):

    clt = MyClient()

    def test_announce(self):
        self.clt.announce("hello")
        self.assertTrue("hello" in buffer)

    def test_display(self):
        evt = Message()
        evt.reply("test1")
        evt.reply("test2")
        self.clt.display(evt)
        self.assertTrue("test1" in buffer)
        self.assertTrue("test2" in buffer)
        self.assertTrue(buffer.index("test1") < buffer.index("test2"))

    def test_dosay(self):
        self.clt.dosay("#channel", "yo!")
        self.assertTrue("yo!" in buffer)

    def test_raw(self):
        pass

    def test_say(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class TestBuffered(unittest.TestCase):

    def start(self):
        pass

    def stop(self):
        pass
