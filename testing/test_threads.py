# This file is placed in the Public Domain.


"threads"


import unittest


from nixt.threads import Thr, Thread


buffer = []


def test():
    buffer.append("test")


class TestThr(unittest.TestCase):

    def test_construct(self):
        thr = Thr(test)
        self.assertTrue(type(thr), Thr)


class TestThread(unittest.TestCase):

    def test_construct(self):
        thread = Thread()
        self.assertTrue(type(thread), Thread)
