# This file is placed in the Public Domain.


"display"


import unittest


from nixt.display import Display, Screen


class TestDisplay(unittest.TestCase):

    def test_construct(self):
        display = Display()
        self.assertTrue(type(display), Display)


class TestScreen(unittest.TestCase):

    def test_construct(self):
        screen = Screen()
        self.assertTrue(type(screen), Screen)
