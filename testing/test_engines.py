# This file is placed in the Public Domain.


"engine"


import unittest


from typing import List


from nixt.defines import Message, Engine


buffer: List[str] = []


def hello(message):
    message.reply(message.text)
    message.ready()


class TestEngine(unittest.TestCase):

    hdl = Engine()

    def setUp(self):
        self.hdl.register("hello", hello)
        self.hdl.start()

    def shutDown(self):
        self.hdl.stop()

    def test_callback(self):
        msg = Message()
        msg.kind = "hello"
        msg.text = "hello"
        self.hdl.handle(msg)
        msg.wait()
        self.assertTrue("hello" in msg.result)

    def test_loop(self):
        msg = Message()
        msg.kind = "hello"
        msg.text = "hello"
        self.hdl.put(msg)
        msg.wait()
        self.assertTrue(msg._ready.is_set())

    def test_loop2(self):
        msg = Message()
        msg.kind = "hello"
        msg.text = "hello bot"
        self.hdl.put(msg)
        msg.wait()
        self.assertTrue("hello bot" in msg.result)

    def test_put(self):
        hdl = Engine()
        msg = Message()
        msg.kind = "hello"
        hdl.put(msg)
        message = hdl.queue.get()
        self.assertTrue(message is msg)

    def test_register(self):
        self.hdl.register("hlo", hello)
        self.assertTrue(hello in self.hdl.cbs.values())

    def test_start(self):
        hdl = Engine()
        hdl.start()
        self.assertTrue(not hdl.stopped.is_set())

    def test_stop(self):
        self.hdl.stop()
        self.assertTrue(self.hdl.stopped.is_set())
