# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0212


"engine"


import unittest


from nixt.handler import Event


class TestMessage(unittest.TestCase):

    def test_ready(self):
        msg = Event()
        msg.ready()
        self.assertTrue(msg._ready.is_set())

    def test_reply(self):
        msg = Event()
        msg.reply("test")
        self.assertTrue("test" in msg.result.values())

    def test_wait(self):
        msg = Event()
        msg.ready()
        msg.wait()
        self.assertTrue(msg._ready.is_set())
