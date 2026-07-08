# This file is placed in the Public Domain.


"if it repeats it's important"


import unittest


from nixt.defines import Repeater


def hello(event):
    event.reply("hoi!")


class TestRepeater(unittest.TestCase):

    def test_construct(self):
        rpt = Repeater()
        self.assertTrue(rpt)

    def test_add(self):
        Repeater.add(60, hello)
        self.assertTrue(Repeater.todo)

    def test_loop(self):
        pass

    def test_start(self):
        pass

    def test_stop(self):
        pass
