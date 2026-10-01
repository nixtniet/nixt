# This file is placed in the Public Domain.


"display"


import unittest


from nixt.display import Display, Screen


class TestDisplay(unittest.TestCase):

    "display unittest"

    def test_construct(self):
        "test display contruction."
        display = Display()
        self.assertTrue(type(display), Display)


class TestScreen(unittest.TestCase):

    "screen unittest"

    def test_construct(self):
        "test screen construction."
        screen = Screen()
        self.assertTrue(type(screen), Screen)
