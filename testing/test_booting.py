# This file is placed in the Public Domain.


"in the beginning"


import unittest


from nixt.defines import Boot, Main, Thread


class TestRuntime(unittest.TestCase):

    def setUp(self):
        self.boot = Boot()
    
    def shutDown(self):
        self.boot.shutdown()

    def test_construct(self):
        self.assertEqual(type(self.boot), Boot)
        
    def test_banner(self):
        self.assertEqual(self.boot.banner(), None)

    def test_configure(self):
        self.assertEqual(self.boot.configure(Main), None)

    def test_forever(self):
        thr = Thread.launch(self.boot.forever)
        self.boot.running.clear()
        thr.join()
        self.assertEqual(self.boot.stopped.is_set(), True)

    def test_init(self):
        self.assertEqual(self.boot.init(""), True)

    def test_shutdown(self):
        thr = Thread.launch(self.boot.shutdown)
        thr.join()
        self.assertTrue(self.boot.stopped.is_set())

    def test_wrapped(self):
        self.assertFalse(self.boot.wrapped(print, "hello world"))
