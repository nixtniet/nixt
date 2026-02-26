# This file is placed in the Public Domain.


"engine"


import unittest


from nixt.message import Message


class TestMessage(unittest.TestCase):

    def test_ready(self):
        msg = Message()
        msg.ready()
        self.assertTrue(msg._ready.is_set())

    def test_reply(self):
        msg = Message()
        msg.reply("test")
        self.assertTrue("test" in msg.result.values())

    def test_wait(self):
        msg = Message()
        msg.ready()
        msg.wait()
        self.assertTrue(msg._ready.is_set())
