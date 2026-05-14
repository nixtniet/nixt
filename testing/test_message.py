# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.event import Event


class TestEvent(unittest.TestCase):

    def test_ready(self):
        msg = Event()
        msg.ready()  # pylint: disable=E1102
        self.assertTrue(msg._ready.is_set())

    def test_reply(self):
        msg = Event()
        msg.reply("test")
        self.assertTrue("test" in msg.result)

    def test_wait(self):
        msg = Event()
        msg.ready()  # pylint: disable=E1102
        msg.wait()
        self.assertTrue(msg._ready.is_set())
