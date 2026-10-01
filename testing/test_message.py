# This file is placed in the Public Domain.


"message"


import unittest


from nixt.defines import Message


class TestMessage(unittest.TestCase):

    "message unittests"

    def test_ready(self):
        "test flagging a message ready."
        msg = Message()
        msg.ready()  # pylint: disable=E1102
        self.assertTrue(msg._ready.is_set())

    def test_reply(self):
        "test replying to a message."
        msg = Message()
        msg.reply("test")
        self.assertTrue("test" in msg.result)

    def test_wait(self):
        "test waiting for a message to complete."
        msg = Message()
        msg.ready() # pylint: disable=E1102
        msg.wait()
        self.assertTrue(msg._ready.is_set())
