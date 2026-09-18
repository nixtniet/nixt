# This file is placed in the Public Domain.


"in the beginning"


import unittest


from nixt.defines import Boot


class TestRuntime(unittest.TestCase):

    def setUp(self):
        self.boot = Boot()
    
    def shutDown(self):
        self.boot.shutdown()

    def test_construct(self):
        self.assertTrue(type(self.boot), Boot)
        
    def test_banner(self):
        pass

    def test_configure(self):
        pass

    def test_forever(self):
        pass

    def test_init(self):
        pass

    def test_shutdown(self):
        pass

    def test_wrapped(self):
        pass
