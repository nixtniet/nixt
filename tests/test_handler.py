# This file is placed in the Public Domain.


import unittest
import time
import threading


from nixt.handler import Event, Handler


class TestEvent(unittest.TestCase):

    def test_event_init(self):
        pass

    def test_event_done(self):
        pass

    def test_event_ready(self):
        pass

    def test_event_reply(self):
        pass

    def test_event_wait(self):
        pass


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.handler = Handler()

    def tearDown(self):
        if not self.handler.stopped.is_set():
            self.handler.stop()

    def test_handler_init(self):
        pass

    def test_register(self):
        pass

    def test_put_and_poll(self):
        pass

    def test_callback(self):
        pass

    def test_callback_no_handler(self):
        pass

    def test_loop(self):
        pass

    def test_start_and_stop(self):
        pass

    def test_wait(self):
        pass


if __name__ == '__main__':
    unittest.main()
