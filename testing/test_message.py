# This file is placed in the Public Domain.


"message"


import unittest


from nixt.defines import Message


class TestMessage(unittest.TestCase):

    "message unittests"

    def test_ready(self):
        "test flagging a message ready."
        msg = Message()
        msg.ready()
        self.assertTrue(msg.__ready__.is_set())

    def test_reply(self):
        "test replying to a message."
        msg = Message()
        msg.reply("test")
        self.assertTrue("test" in msg.result)

    def test_wait(self):
        "test waiting for a message to complete."
        msg = Message()
        msg.ready()
        msg.wait()
        self.assertTrue(msg.__ready__.is_set())
