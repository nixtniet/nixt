# This file is placed in the Public Domain.


"threads"


import unittest


from nixt.threads import Thr, Thread


buffer = []


def test():
    "append to buffer."
    buffer.append("test")


class TestThr(unittest.TestCase):

    "thr unittests"

    def test_construct(self):
        "test thr construction." 
        thr = Thr(test)
        self.assertTrue(type(thr), Thr)


class TestThread(unittest.TestCase):

    "thread unittests"

    def test_construct(self):
        "test thread construction."
        thread = Thread()
        self.assertTrue(type(thread), Thread)
