# This file is placed in the Public Domain.


"logging tests"


import unittest


from nixt.defines import Config, Main


class TestConfig(unittest.TestCase):

    def test_construct(self):
        config = Config("test", (), {})
        self.assertTrue(type(config), Config)


class TestMain(unittest.TestCase):

    def test_construct(self):
        main = Main()
        self.assertTrue(type(main), Main)

    def test_main(self):
        Main.a = "b"
        self.assertEqual(Main.a, "b")

    def test_missing(self):
        self.assertFalse(Main.b)
